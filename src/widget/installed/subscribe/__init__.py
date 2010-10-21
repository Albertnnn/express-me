#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Feed Widget that display rss or atom feed.
'''

import widget

class Widget(widget.WidgetModel):
    '''
    Show rss or atom feed
    '''
    widget_name = 'Subscribe'
    widget_author = 'Michael Liao'
    widget_description = 'Subscribe the feed'
    widget_url = 'http://michael.liaoxuefeng.com/'

    def get_content(self):
        url = shared.get_setting('blog_setting', 'feed_proxy', '/blog/feed')
        return '<div><a href="%s"><img src="/widget/installed/subscribe/static/feed.gif" width="16" height="16" style="vertical-align:middle" /></a> <a href="%s" target="_blank">Subscribe to Feed</a></div>' % (url, url)
