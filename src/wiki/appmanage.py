#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Wiki app management.
'''

import wiki

from exweb import context

from manage import shared

import manage

appmenus = [
        ('Wiki', [
                shared.AppMenuItem(shared.USER_ROLE_CONTRIBUTOR, 'Pages', 'edit_pages'),
                shared.AppMenuItem(shared.USER_ROLE_CONTRIBUTOR, 'Settings', 'settings')
        ])
]

def manage_nav():
    '''
    Get app's navigation settings so user can customize their navigation bar.
    
    Returns:
        A list contains (title, url).
    '''
    return [('Wiki', '/wiki/')]

def manage_app(user, action, **args):
    f = ''.join(['__handle_', context.method, '_', action, '()'])
    # we are going to call function by name '__handle_' + (get or post) + _ + action
    return eval(f)

def __handle_get_edit_pages():
    COUNT = 20
    pages = None
    prev = context.query.get('prev', '')
    if prev:
        # show previous page:
        pages = wiki.WikiPage.all().filter('wiki_title <', prev).order('-wiki_title').fetch(COUNT+1)
        has_prev = len(pages)>COUNT
        next = pages[0]
        return
    # show next page:
    next = context.query.get('next', '')
    has_prev = False
    if next:
        pages = wiki.WikiPage.all().filter('wiki_title >=', next).order('wiki_title').fetch(COUNT+1)
        has_prev = True
    else:
        pages = wiki.WikiPage.all().order('wiki_title').fetch(COUNT+1)
    has_next = len(pages)>COUNT
    next_pos = None
    if has_next:
        next_pos = pages.pop()
    return {
            'template' : 'page_list.html',
            'pages' : pages,
            'has_prev' : has_prev,
            'has_next' : has_next,
            'next_pos' : next_pos
    }

def __handle_get_settings():
    '''
    show form of settings of wiki
    '''
    return {
            'template' : 'setting.html',
            'entry' : shared.get_setting('wiki', 'entry', 'Main Page'),
            'edit_level' : '',
            'approve_level' : ''
    }

def __handle_post_settings():
    '''
    update settings of wiki
    '''
    entry = context.form.get('entry', 'Main Page')
    shared.save_setting('wiki', 'entry', entry)
    dict = __handle_get_settings();
    dict['message'] = 'Your wiki settings are saved.'
    return dict
