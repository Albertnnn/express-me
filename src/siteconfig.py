#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Load site info.
'''

import logging

from framework import cache
from framework import store

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

    __slots__ = ('title', 'subtitle', 'date_format', 'time_format', 'time_zone')

    defaults = {
            'title' : 'ExpressMe',
            'subtitle' : 'just another ExpressMe web site',
            'date_format' : DEFAULT_DATE,
            'time_format' : DEFAULT_TIME,
            'time_zone' : '',
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
        logging.info('%s=%s' % (key, getattr(site, key)))
        store.set_setting(key, getattr(site, key), SITE_GROUP)
    cache.delete(SITE_GROUP)

def _get_from_store():
    site_dict = store.get_settings(SITE_GROUP)
    kw = {}
    for k in site_dict.keys():
        kw[str(k)] = site_dict[k]
    return Site(**kw)

def tz_list():
    tzs = (
            '(UTC-12:00) International Date Line West',
            '(UTC-11:00) Coordinated Universal Time-11',
            '(UTC-11:00) Samoa',
            '(UTC-10:00) Hawaii',
            '(UTC-09:00) Alaska',
            '(UTC-08:00) Baja California',
            '(UTC-08:00) Pacific Time (US & Canada)',
            '(UTC-07:00) Arizona',
            '(UTC-07:00) Chihuahua, La Paz, Mazatlan',
            '(UTC-07:00) Mountain Time (US & Canada)',
            '(UTC-06:00) Central America',
            '(UTC-06:00) Central Time (US & Canada)',
            '(UTC-06:00) Guadalajara, Mexico City, Monterrey',
            '(UTC-06:00) Saskatchewan',
            '(UTC-05:00) Bogota, Lima, Quito',
            '(UTC-05:00) Eastern Time (US & Canada)',
            '(UTC-05:00) Indiana (East)',
            '(UTC-04:30) Caracas',
            '(UTC-04:00) Asuncion',
            '(UTC-04:00) Atlantic Time (Canada)',
            '(UTC-04:00) Cuiaba',
            '(UTC-04:00) Georgetown, La Paz, Manaus, San Juan',
            '(UTC-04:00) Santiago',
            '(UTC-03:30) Newfoundland',
            '(UTC-03:00) Brasilia',
            '(UTC-03:00) Buenos Aires',
            '(UTC-03:00) Cayenne, Fortaleza',
            '(UTC-03:00) Greenland',
            '(UTC-03:00) Montevideo',
            '(UTC-02:00) Coordinated Universal Time-02',
            '(UTC-',
            '(UTC-',
            '(UTC-',
            '(UTC-',
            '(UTC-',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
    )