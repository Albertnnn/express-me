#!/usr/bin/env python
# -*- coding: utf-8 -*-

import widget

name = 'HTML Snippet'
author = 'Michael Liao'
description = 'Display any HTML snippet'
url = 'http://michael.liaoxuefeng.com/'

class Widget(widget.WidgetModel):
    '''
    Show any html snippet.
    '''
    title = widget.WidgetSetting(description='Widget title')
    content = widget.WidgetSetting(description='Any HTML snippet', default='<p>Your html snippet goes here...</p>')

    def load(self):
        html = r'<div><a href="http://feeds.feedburner.com/expressme"><img src="http://feeds.feedburner.com/~fc/expressme?bg=66FFCC&amp;fg=333333&amp;anim=0" height="26" width="88" style="border:0" alt="" /></a></div>'
        return {
                'title' : self.title,
                'content' : self.content
        }
