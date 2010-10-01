#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
app that do management.
'''

from time import time

import hashlib
import base64
import os

from google.appengine.ext import db
from exweb import context
from manage import shared

from framework import ApplicationError

class PermissionError(ApplicationError):
    pass

class Page(object):
    def __init__(self, page_index, page_size, total=(-1)):
        assert page_index>0
        assert page_size>0 and page_size<=100
        self.page_index = page_index
        self.page_size = page_size
        self.has_prev = page_index>1

class UserMeta(db.Model):
    'settings for website'
    meta_key = db.StringProperty(required=True)
    meta_values = db.StringListProperty()

# cookie constants:

COOKIE_AUTO_SIGN_ON = '_auto_signon_'
COOKIE_EXPIRES_MIN = 86400
COOKIE_EXPIRES_MAX = 31536000

NAV_MAX = 10

def get_navigations():
    '''
    Get navigation definitions with [(title, url), (...), ...].
    
    Returns:
        A list contains multiple tuple of (title, url).
    '''
    navs = shared.get_settings('navigation')
    if not navs:
        import appconfig
        return [(x, '/' + x) for x in appconfig.apps]
    navigations = []
    for i in range(NAV_MAX):
        title = ''
        title_key = 'title_%d' % i
        if title_key in navs:
            title = navs[title_key]
        url = ''
        url_key = 'url_%d' % i
        if url_key in navs:
            url = navs[url_key]
        if title and url:
            navigations.append((title, url))
    return navigations

def get_themes():
    root = os.path.split(os.path.dirname(__file__))[0]
    theme_root = os.path.join(root, 'theme')
    themes = os.listdir(theme_root)
    valid_themes = [theme for theme in themes if __is_valid_theme(theme_root, theme)]
    valid_themes.sort()
    return valid_themes

def __is_valid_theme(theme_root, theme):
    dir = os.path.join(theme_root, theme)
    file = os.path.join(dir, 'template.html')
    return os.path.isdir(dir) and os.path.isfile(file)
