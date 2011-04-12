#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
App "blog" that supports publishing posts and pages.
'''

from framework import store

GROUP_OPTIONS = 'blog.post.options'

FEED_TITLE = 'feed_title'
FEED_PROXY = 'feed_proxy'
FEED_ITEMS = 'feed_items'
SHOW_ABSTRACT = 'show_abstract'

def get_feed_url():
    '''
    Get feed url
    '''
    feed_proxy = store.get_setting(FEED_PROXY, GROUP_OPTIONS, '')
    if not feed_proxy:
        feed_proxy = '/blog/feed'
    return feed_proxy

def get_feed_html():
    '''
    Get feed html in <head>...</head>.
    '''
    feed_title = store.get_setting(FEED_TITLE, GROUP_OPTIONS, 'Posts')
    feed_proxy = get_feed_url()
    return r'<link href="%s" title="%s" type="application/rss+xml" rel="alternate" />' % (feed_proxy, feed_title)

def update_default_settings(options):
    '''
    Fill default settings if options do not contain.
    '''
    for k, v in (('show_abstract', 'False'), (FEED_PROXY, ''), (FEED_ITEMS, '20'), (FEED_TITLE, 'Posts')):
        if not k in options:
            options[k] = v
