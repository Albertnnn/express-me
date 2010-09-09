#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Blog utils
'''

from exweb import HttpNotFoundError

from manage import shared

def assert_not_none(o):
    if o is None:
        raise HttpNotFoundError()

def get_feed():
    ''' get feed url and title '''
    url = shared.get_setting('blog_setting', 'feed_proxy', '/blog/feed')
    title = shared.get_setting('blog_setting', 'feed_title', 'Rss Feed')
    return { 'url' : url, 'title' : title }

def format_rss_date(dt):
    # format: Sun, 07 Feb 2010 20:56:30
    return dt.strftime('%a, %d %b %Y %H:%M:%S')
