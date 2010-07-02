#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Wiki app that display wiki pages.
'''

import urllib

from exweb import context
from exweb import get
from exweb import mapping
from exweb import raw_mapping

import manage
import wiki
from wiki import parser

def __to_unicode(raw):
    return raw.decode('utf8')

def __url_encode(uni_string):
    return urllib.quote(uni_string.encode('utf8'), '')

@get('/')
def get_main_page():
    '''
    show main page of wiki
    '''
    entry = manage.get_setting('wiki', 'entry', '')
    if not entry:
        entry = 'Main Page'
    return get_page(entry)

@raw_mapping(r'\/page\/(.*)')
def get_page(utf8title):
    '''
    show page by title.
    '''
    title = __to_unicode(utf8title)
    content = ''
    page = wiki.get_wiki(title)
    if page is not None:
        content = parser.parse(page.wiki_content, wiki.has_wiki)
    editable = page is not None and context.user is not None
    if editable:
        editable = page.wiki_state!=wiki.WIKI_LOCKED or context.user.user_role==manage.USER_ROLE_ADMINISTRATOR
    return {
            'editable' : editable,
            'title' : title,
            'content' : content,
            'url_encode': __url_encode
    }

@mapping('/edit')
def edit_page():
    '''
    Edit a new page or exist page.
    '''
    utf8title = context.request.get('title', '')
    title = __to_unicode(utf8title)
    if context.user is None:
        return 'redirect:/manage/signin?redirect=/wiki/edit%3Ftitle%3D' + __url_encode(title)
    if context.method=='get':
        content = ''
        page = wiki.get_wiki(title)
        if page is not None:
            content = page.wiki_content
        return {
                'edit' : True,
                'title' : title,
                'content' : content,
                'url_encode': __url_encode
        }
    # update wiki:
    content = context.request.get('content', '')
    try:
        wiki.edit_wiki(context.user, title, content)
        return 'redirect:/wiki/page/%s' % __url_encode(title)
    except wiki.WikiError, e:
        pass
