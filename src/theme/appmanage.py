#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Theme app management.
'''

import logging

from framework import store

from manage import AppMenu
from manage import AppMenuItem

import theme

def get_menus():
    '''
    Get menus for management.
    '''
    theme = AppMenu('Theme',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Edit', 'edit_theme'),
    )
    return (theme,)

def _edit_theme(user, app, context):
    if context.method=='get':
        themes = theme.get_themes(False)
        return {
                '__view__' : 'manage_edit_theme',
                'current' : theme.get_theme(),
                'themes' : [theme.get_theme_info(t) for t in themes],
        }
    if context.method=='post':
        title = context.get_argument('title')
        content = context.get_argument('content')
        category = context.get_argument('category')
        tags = context.get_argument('tags')
        draft = context.get_argument('draft')=='True'
        allow_comment = context.get_argument('allow_comment')=='True'
        state = model.POST_PUBLISHED
        if draft:
            state = model.POST_DRAFT
        p = model.create_post(user, state, title, content, model.get_category(category), tags, allow_comment)
        return __json_result(True, p)

def manage(user, app, command, context):
    map = {
           'edit_theme' : _edit_theme,
    }
    return map[command](user, app, context)
