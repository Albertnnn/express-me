#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Common functions and classes used for app management.
'''

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

class AppMenu(object):
    '''
    A menu object displayed in management console.
    '''
    def __init__(self, title, *menu_items):
        self.title = title
        self.items = []
        self.items.extend(menu_items)

class AppMenuItem(object):
    '''
    A menu item that belongs to an AppMenu.
    '''
    def __init__(self, role, title, command):
        self.role = role
        self.title = title
        self.command = command
