#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
httptest package for testing web framework of ExpressMe.
'''

from framework.web import get
from framework.web import post
from framework.web import mapping

@get('/')
def http_home():
    return '<h1>Home</h1>'

@post('/hello/$')
def http_hello(name):
    return '<p>Hello, %s!</p>' % name

@mapping('/hi/$')
def hi(name):
    return '<p>Hi, %s!</p>' % name

@get('/redirect/$')
def http_redirect(target):
    return 'redirect:/about/%s' % target

@get('/args')
def http_args(**kw):
    ctx = kw['context']
    return u'%s, %s, %s, [%s, %s]' % (
            ctx.get_argument('q'),
            ctx.get_argument('ref'),
            ctx.get_argument('src'),
            ctx.get_arguments('nl')[0],
            ctx.get_arguments('nl')[1],
    )
