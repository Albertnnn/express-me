#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
app management for user, global settings.
'''

from framework import store

from manage.common import AppMenu
from manage.common import AppMenuItem

def get_menus():
    user = AppMenu('User',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Edit', 'edit_user'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Add New', 'add_user'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Your Profile', 'profile')
    )
    setting = AppMenu('Setting',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Site Info', 'site'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Navigation', 'navigation'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Theme', 'theme'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Storage', 'storage')
    )
    return (user, setting,)

def _edit_user(user, command, **kw):
    pass

def manage(user, command, **kw):
    map = {
           'edit_user' : _edit_user
    }
