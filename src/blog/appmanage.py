#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Blog app management.
'''

from framework import store

from blog import model

from manage.common import AppMenu
from manage.common import AppMenuItem

def get_menus():
    '''
    Get menus for management.
    '''
    post = AppMenu('Post',
            AppMenuItem(store.ROLE_CONTRIBUTOR, 'Edit', 'edit_post'),
            AppMenuItem(store.ROLE_CONTRIBUTOR, 'Add New', 'add_post'),
            AppMenuItem(store.ROLE_CONTRIBUTOR, 'Tags', 'tags')
    )
    page = AppMenu('Page',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Edit', 'edit_page'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Add New', 'add_page')
    )
    return (post, page,)

def _edit_post(user, app, context):
    pass

def _add_post(user, app, context):
    if context.method=='get':
        categories = model.get_categories()
        return {
                '__view__' : 'manage_editor',
                'static' : False,
                'post' : {
                        'id' : '',
                        'static' : False,
                        'title' : '',
                        'content' : '',
                        'ref' : user.id,
                        'author' : user.nicename,
                        'tags_as_string' : lambda : '',
                },
                'categories' : categories,
        }

def manage(user, app, command, context):
    map = {
           'edit_post' : _edit_post,
           'add_post' : _add_post,
    }
    return map[command](user, app, context)
