#!/usr/bin/env python
# -*- coding: utf-8 -*-

import widget

class Widget(widget.WidgetModel):

    __title__ = 'HTML Snippet'
    __author__ = 'Michael Liao'
    __description__ = 'Display any HTML snippet'
    __url__ = 'http://www.expressme.org/'

    '''
    Show any html snippet.
    '''
    title = widget.WidgetSetting(description='Widget title')
    content = widget.WidgetSetting(description='Any HTML snippet', default='<p>Your html snippet goes here...</p>')

    def get_content(self):
        return r'<div><a href="http://feeds.feedburner.com/expressme"><img src="http://feeds.feedburner.com/~fc/expressme?bg=66FFCC&amp;fg=333333&amp;anim=0" height="26" width="88" style="border:0" alt="" /></a></div>'
