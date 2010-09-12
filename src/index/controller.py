#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Handle index page '/'.
'''

from framework.web import get

@get('/')
def index():
    return '<h1>just an index page</h1>'
