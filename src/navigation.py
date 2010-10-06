#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Load navigation menu.
'''

from framework import cache
from framework import store

NAV_GROUP = '__navigation__'

def get_navigation(use_cache=True):
    '''
    Get navigation as a list contains ('title', 'url').
    
    Args:
        use_cache: True if use cache, default to True.
    '''
    if use_cache:
        return cache.get(NAV_GROUP, _get_from_store, 3600)
    return _get_from_store()

def set_navigation(navs):
    '''
    Set navigations. The old will be removed.
    
    Args:
        navs: list contains ('title', 'url').
    '''
    store.delete_settings(NAV_GROUP)
    n = 0
    for title, url in navs:
        store.set_setting(u'%02d%s' % (n, title,), url, NAV_GROUP)
        n = n + 1
    cache.delete(NAV_GROUP)

def _get_from_store():
    nav_dict = store.get_settings(NAV_GROUP)
    if not nav_dict:
        nav_dict[u'00Home'] = u'/'
    # sort:
    keys = nav_dict.keys()
    keys.sort()
    navs = []
    for key in keys:
        if len(key)>2:
            navs.append((key[2:], nav_dict[key],))
    return navs
