#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
app management for user, global settings.
'''

import datetime

import appconfig
import navigation
import siteconfig

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

def __get_edit_user(user, app, context):
    role = context.get_argument('role', '')
    if role=='':
        role = None
    else:
        role = int(role)
    offset = context.get_argument('offset', '')
    index = 1
    if offset:
        index = int(context.get_argument('index'))
    users, next_cursor = store.get_users(4, offset, role=role)
    return {
            '__view__' : 'manage_edit_user',
            'users' : users,
            'role' : role,
            'offset' : offset,
            'next' : next_cursor,
            'index' : index,
    }

def _edit_user(user, app, context):
    if context.method=='get':
        return __get_edit_user(user, app, context)
    if context.method=='post':
        btn = context.get_argument('btn')
        user_ids = context.get_arguments('u')
        if btn=='lock' or btn=='unlock':
            store.lock_or_unlock_users(user_ids, btn=='lock')
            return __get_edit_user(user, app, context)
        if btn=='set_role':
            role = int(context.get_argument('set_role'))
            for id in user_ids:
                user = store.get_user_by_key(id)
                user.role = role
                user.put()
            return __get_edit_user(user, app, context)

def __get_navigation(context):
    selections = [('- Select -', '#'), ('Home', '/')]
    for appname in appconfig.apps:
        mod = __import__(appname, fromlist=['appmanage']).appmanage
        get_nav = getattr(mod, 'get_navigation', None)
        if callable(get_nav):
            selections.extend([(title, '/' + appname + url) for title, url in get_nav()])
    selections.append(('Custom', ''))
    navs = navigation.get_navigation(False)
    if len(navs)<10:
        for i in range(10 - len(navs)):
            navs.append(('', '',))
    return {
            '__view__' : 'manage_navigation',
            'selections' : selections,
            'navigations' : navs,
    }

def _navigation(user, app, context):
    if context.method=='get':
        return __get_navigation(context)
    if context.method=='post':
        L = []
        for i in range(10):
            title = context.get_argument('title_%d' % i)
            url = context.get_argument('url_%d' % i)
            if title and url:
                L.append((title, url,))
        navigation.set_navigation(L)
        return __get_navigation(context)

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

def _site(user, app, context):
    if context.method=='get':
        site = siteconfig.get_site_settings(False)
        dt = datetime.datetime.now()
        return {
                '__view__' : 'manage_site',
                'site' : site,
                'date_formats' : siteconfig.date_format_samples(dt),
                'time_formats' : siteconfig.time_format_samples(dt),
        }

def manage(user, app, command, context):
    map = {
           'edit_user' : _edit_user,
           'profile' : _profile,
           'navigation' : _navigation,
           'site' : _site,
    }
    return map[command](user, app, context)
