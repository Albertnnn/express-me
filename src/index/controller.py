#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Handle index page '/'.
'''

from framework.web import get

from blog import controller as blog_controller
from blog import model as blog_model

@get('/')
def index(**kw):
    '''
    show recent posts of blog
    '''
    ctx = kw['context']
    number = 20
    posts, next = blog_model.get_posts(number, None)
    return {
            '__theme__' : True,
            '__view__' : 'index',
            '__title__' : 'Home',
            '__header__' : blog_controller.get_feed_html(),
            'posts' : posts,
    }
