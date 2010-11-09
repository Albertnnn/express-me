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
                'current' : theme.get_current_theme(),
                'themes' : [theme.get_theme_info(t) for t in themes],
        }
    if context.method=='post':
        pass

def manage(user, app, command, context):
    map = {
           'edit_theme' : _edit_theme,
    }
    return map[command](user, app, context)
