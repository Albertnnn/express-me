#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Widget app that dispatch requests to widget.
'''

from exweb import mapping
from exweb import context
from exweb import HttpNotFoundError

@mapping('/$/')
def handle_widget2(module_name):
    return handle_widget(module_name)

@mapping('/$')
def handle_widget(module_name):
    '''
    Handle url using specified widget module.
    '''
    try:
        m = __import__('widget.' + module_name, fromlist=['Widget'])
    except ImportError:
        raise HttpNotFoundError()
    w = m.Widget()
    parameters = {}
    w.handle_request(context.request, context.response, parameters)
