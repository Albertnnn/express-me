#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Wiki app
'''

from datetime import datetime

from google.appengine.ext import db
from manage import shared

WIKI_EDITABLE = 0  # wiki is open to edit
WIKI_PROTECTED = 1 # wiki can be edit, but need approval by admin
WIKI_LOCKED = 2    # wiki cannot be edit
WIKI_PENDING = 10  # wiki is pending for approval

class WikiError(StandardError):
    def __init__(self, message):
        self.message = message

class WikiHistory(db.Model):
    wiki_user = db.ReferenceProperty(reference_class=shared.User, required=True)
    wiki_title = db.StringProperty(required=True)
    wiki_content = db.TextProperty(required=True)
    wiki_date = db.DateTimeProperty()
    wiki_state = db.IntegerProperty()

class WikiPage(db.Model):
    wiki_history = db.ReferenceProperty(reference_class=WikiHistory, required=True)
    wiki_title = db.StringProperty(required=True)
    wiki_content = db.TextProperty(required=True)
    wiki_date = db.DateTimeProperty()
    wiki_modified = db.DateTimeProperty()
    wiki_state = db.IntegerProperty(required=True, default=WIKI_EDITABLE)

def has_wiki(title):
    '''
    Is wiki exist and visible.
    
    Args:
        title: wiki title, unicode.
    
    Returns:
        True if exist, otherwise False.
    '''
    list = WikiPage.all().filter('wiki_title =', title).filter('wiki_state <', WIKI_PENDING).fetch(1)
    return len(list)>0

def get_wiki(title):
    '''
    Get wiki page by title.
    
    Args:
        title: wiki title, unicode.
    
    Returns:
        WikiPage object, or None if not exist.
    '''
    list = WikiPage.all().filter('wiki_title =', title).filter('wiki_state <', WIKI_PENDING).fetch(1)
    if list:
        return list[0]
    return None

def edit_wiki(user, title, content):
    '''
    Create or update a wiki page.
    
    Args:
        user: user object.
        title: page title, unicode.
        content: page content.
    
    Returns:
        True if page is visible, False otherwise.
    '''
    now = datetime.now()
    list = WikiPage.all().filter('wiki_title =', title).fetch(1)
    if list:
        page = list[0]
        if page.wiki_state==WIKI_LOCKED and user.user_role!=shared.USER_ROLE_ADMINISTRATOR:
            raise WikiError('Wiki page is locked.')
        approved = page.wiki_state==WIKI_EDITABLE or user.user_role<=shared.USER_ROLE_EDITOR
        # add a new history only:
        history = WikiHistory(wiki_user=user, wiki_title=title, wiki_content=content, wiki_date=now, wiki_approved=approved)
        history.put()
        if approved:
            page.wiki_history = history
            page.wiki_modified = now
            page.wiki_content = content
            # change pending state to visible:
            if page.wiki_state==WIKI_PENDING:
                page.wiki_state = WIKI_EDITABLE
            page.put()
        return page.wiki_state!=WIKI_PENDING
    # create a new wiki page:
    approved = user.user_role<=shared.USER_ROLE_EDITOR
    history = WikiHistory(wiki_user=user, wiki_title=title, wiki_content=content, wiki_date=now, wiki_approved=approved)
    history.put()
    page = WikiPage(wiki_history=history, wiki_title=title, wiki_content=content, wiki_date=now, wiki_modified=now)
    if not approved:
        page.wiki_state = WIKI_PENDING
    page.put()
    return page.wiki_state!=WIKI_PENDING
