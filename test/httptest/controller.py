#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
httptest package for testing web framework of ExpressMe.
'''

from framework.web import get
from framework.web import post

@get('/')
def http_home():
    return '<h1>Home</h1>'

@post('/hello/$')
def http_hello(name):
    return '<p>Hello, %s!</p>' % name

@get('/redirect/$')
def http_redirect(target, **kw):
    return 'redirect:/about/%s/%s' % (target, kw['request'].method.lower())
