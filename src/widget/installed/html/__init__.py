#!/usr/bin/env python
# -*- coding: utf-8 -*-

import widget

class Widget(widget.WidgetModel):
    '''
    Show any html snippet.
    '''

    __title__ = 'HTML Snippet'
    __author__ = 'Michael Liao'
    __description__ = 'Display any HTML snippet'
    __url__ = 'http://www.expressme.org/'

    @staticmethod
    def get_settings():
        return [widget.WidgetSetting(key='html', description='Any HTML snippet', default='<p>Your html snippet goes here...</p>')]

    def get_content__raw__(self):
        return self.html
