#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Load site info.
'''

from framework import cache
from framework import store

SITE_GROUP = '__site__'

class Site(object):
    '''
    Site object that has attributes such as 'title', 'subtitle', etc.
    '''

    __slots__ = ('title', 'subtitle', 'date_format', 'time_format', 'timezone')

    defaults = {
            'title' : 'ExpressMe',
            'subtitle' : 'just another ExpressMe web site',
            'date_format' : '',
            'time_format' : '',
            'timezone' : '',
    }

    def __init__(self, **kw):
        for key in self.__slots__:
            if key in kw:
                setattr(self, key, kw[key])
            else:
                setattr(self, key, Site.defaults[key])

def get_site_settings(use_cache=True):
    '''
    Get site as a site object which has attribute of 'title', 'subtitle', etc.
    
    Args:
        use_cache: True if use cache, default to True.
    '''
    if use_cache:
        return cache.get(SITE_GROUP, _get_from_store, 3600)
    return _get_from_store()

def set_site_settings(**kw):
    '''
    Set site info.
    
    Args:
        keyword args support 'title', 'subtitle', etc.
    '''
    store.delete_settings(SITE_GROUP)
    site = Site(**kw)
    for key in site.__slots__:
        store.set_setting(key, getattr(site, key), SITE_GROUP)
    cache.delete(SITE_GROUP)

def _get_from_store():
    site_dict = store.get_settings(SITE_GROUP)
    return Site(**site_dict)
