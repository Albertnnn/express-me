#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Load site info.
'''

import logging

from framework import cache
from framework import store
from util import dt

SITE_GROUP = '__site__'

DEFAULT_DATE = '%Y-%m-%d'
DEFAULT_TIME = '%H:%M:%S'

def date_format_samples(dt):
    '''
    Return date format samples with list of tuple (format, sample).
    '''
    formats = (DEFAULT_DATE, '%y-%m-%d', '%d/%m/%Y', '%d/%m/%y', '%m/%d/%Y', '%m/%d/%y', '%b %d, %Y', '%b %d, %y', '%B %d, %Y', '%B %d, %y')
    return [(f, dt.strftime(f)) for f in formats]

def time_format_samples(dt):
    '''
    Return time format samples with list of tuple (format, sample).
    '''
    formats = (DEFAULT_TIME, '%H:%M', '%I:%M:%S %p', '%I:%M %p')
    return [(f, dt.strftime(f)) for f in formats]

class Site(object):
    '''
    Site object that has attributes such as 'title', 'subtitle', etc.
    '''

    __slots__ = ('title', 'subtitle', 'date_format', 'time_format', 'tz_name', 'tz_h_offset', 'tz_m_offset', 'tz_dst')

    defaults = {
            'title' : 'ExpressMe',
            'subtitle' : 'just another ExpressMe web site',
            'date_format' : DEFAULT_DATE,
            'time_format' : DEFAULT_TIME,
            'tz_name' : dt.UTC_NAME,
            'tz_h_offset' : 0,
            'tz_m_offset' : 0,
            'tz_dst' : 0,
    }

    def __init__(self, **kw):
        for key in self.__slots__:
            if key in kw:
                setattr(self, key, kw[key])
            else:
                setattr(self, key, Site.defaults[key])

    def get_tzinfo(self):
        return dt.UserTimeZone(self.tz_name, int(self.tz_h_offset), int(self.tz_m_offset), int(self.tz_dst))

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
        store.set_setting(key, str(getattr(site, key)), SITE_GROUP)
    cache.delete(SITE_GROUP)

def _get_from_store():
    site_dict = store.get_settings(SITE_GROUP)
    kw = {}
    for k in site_dict.keys():
        kw[str(k)] = site_dict[k]
    return Site(**kw)
