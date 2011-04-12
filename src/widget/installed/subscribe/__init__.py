#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Feed Widget that display rss or atom feed.
'''

import blog
import widget

class Widget(widget.WidgetModel):
    '''
    Show rss or atom feed
    '''
    __title__ = 'Subscribe To'
    __author__ = 'Michael Liao'
    __description__ = 'Subscribe the feed to readers'
    __url__ = 'http://www.expressme.org/'

    @staticmethod
    def get_settings():
        return []

    def get_content__raw__(self):
        feed = blog.model.get_feed_url()
        url = framework.store.get_setting('blog_setting', 'feed_proxy', '/blog/feed')
        return '<div><a href="%s"><img src="/widget/installed/subscribe/static/feed.gif" width="16" height="16" style="vertical-align:middle" /></a> <a href="%s" target="_blank">Subscribe to Feed</a></div>' % (url, url)
