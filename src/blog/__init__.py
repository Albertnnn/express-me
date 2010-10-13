#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
App "blog" that supports publishing posts and pages.
'''

GROUP_OPTIONS = 'blog.post.options'

FEED_TITLE = 'feed_title'
FEED_PROXY = 'feed_proxy'
FEED_ITEMS = 'feed_items'
SHOW_ABSTRACT = 'show_abstract'

def update_default_settings(options):
    '''
    Fill default settings if options do not contain.
    '''
    for k, v in (('show_abstract', 'False'), (FEED_PROXY, ''), (FEED_ITEMS, '20'), (FEED_TITLE, 'Posts')):
        if not k in options:
            options[k] = v
