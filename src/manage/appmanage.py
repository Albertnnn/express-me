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

def _edit_user(user, app, context):
    if context.method=='get':
        offset = context.get_argument('offset', '')
        users, next_cursor = store.get_users(4, offset)
        return {
                '__view__' : 'manage_edit_user',
                'users' : users,
                'offset' : offset,
                'next' : next_cursor,
        }

def _profile(user, app, context):
    if context.method=='post':
        nicename = context.get_argument('nicename')
        password = context.get_argument('password', '')
        profile_changed = False
        password_changed = False
        if user.nicename!=nicename:
            user.nicename = nicename
            profile_changed = True
        if password and user.password!=password:
            user.password = password
            password_changed = True
        if profile_changed or password_changed:
            user.put()
        msg = 'Your profile has been saved.'
        if password_changed:
            msg = 'Your profile and password have been saved.'
        return {
            '__view__' : 'manage_profile',
            'info' : msg,
        }
    return {
            '__view__' : 'manage_profile',
    }

def manage(user, app, command, context):
    map = {
           'edit_user' : _edit_user,
           'profile' : _profile,
    }
    return map[command](user, app, context)
