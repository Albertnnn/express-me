#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
app management.
'''

from framework import store

from manage.common import AppMenu
from manage.common import AppMenuItem

def get_menus():
    menu = AppMenu('Sample',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Command 1', 'cmd_1'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Command 2', 'cmd_2'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Your Profile', 'profile')
    )
    return (menu,)

def get_navigation():
    return [('Sample', '/')]

def _cmd_1(user, command, **kw):
    pass

def manage(user, command, **kw):
    map = {
           'cmd_1' : _cmd_1
    }
