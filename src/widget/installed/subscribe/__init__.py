#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Feed Widget that display rss or atom feed.
'''

import manage
import widget

title = 'Subscribe'
description = 'Display a subscribe link to subscribe the feed'

class Widget(widget.WidgetModel):
    '''
    Show rss or atom feed
    '''
    def get_content(self):
        url = manage.get_setting('blog_setting', 'feed_proxy', '/blog/feed')
        return '<div><a href="%s"><img src="/widget/subscribe/static/feed.gif" width="16" height="16" style="vertical-align:middle" /></a> <a href="%s" target="_blank">Subscribe to Feed</a></div>' % (url, url)
