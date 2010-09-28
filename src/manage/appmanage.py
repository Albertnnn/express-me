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
    '''
    Get menus for management.
    '''
    user = AppMenu('User',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Edit', 'edit_user'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Add New', 'add_user'),
            AppMenuItem(store.ROLE_SUBSCRIBER, 'Your Profile', 'profile')
    )
    setting = AppMenu('Setting',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Site Info', 'site'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Navigation', 'navigation'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Theme', 'theme'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Storage', 'storage')
    )
    return (user, setting,)

def _profile(user, app, context):
    if context.method=='post':
        nicename = context.get_argument('nicename')
        #password = context.get_argument('password')
    return {
            '__view__' : 'manage_profile',
    }

def manage(user, app, command, context):
    map = {
           'profile' : _profile
    }
    return map[command](user, app, context)
