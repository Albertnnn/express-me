#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
app that manage User and core data in datastore and handle sign on.
'''

from time import time

import hashlib
import base64
import os

from google.appengine.ext import db
from exweb import context
from manage import shared

class AppMenu(object):
    '''
    A menu object displayed in management console.
    '''
    def __init__(self, title):
        self.title = title

class AppMenuItem(object):
    '''
    A menu item that belongs to an AppMenu.
    '''
    def __init__(self, role, title, action):
        self.role = role
        self.title = title
        self.action = action

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

def datetime_format(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')

def date_format(date):
    return date.strftime('%Y-%m-%d')

def time_format(time):
    return time.strftime('%H:%M:%S')

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

def get_user(key):
    '''
    Get User object by key.
    
    Args:
        key: key as string.
    
    Returns:
        User object or None if not found.
    '''
    return shared.User.get(key)

def make_sign_on_cookie(key, passwd, expire_in_seconds):
    # make sign on cookie with following format:
    # base64(id_expires_md5(id_expires_passwd))
    expires = int(time()) + expire_in_seconds
    md5 = hashlib.md5(key + '_' + str(expires) + '_' + passwd).hexdigest()
    return base64.b64encode(key + '_' + str(expires) + '_' + md5)

def validate_sign_on_cookie(value, get_user):
    '''
    Validate signon cookie.
    
    Args:
        value: cookie value, a base64-encoded string.
        get_user: function for get User object by key.
    
    Returns:
        User object if sign on ok, None if cookie is invalid.
    '''
    dec = base64.b64decode(value)
    ss = dec.split('_')
    if len(ss)!=3:
        return None
    key = ss[0]
    expires = ss[1]
    try:
        if int(expires)<time():
            return None
    except ValueError:
        return None
    user = get_user(key)
    if user is None:
        return None
    md5 = hashlib.md5(key + '_' + expires + '_' + user.user_passwd).hexdigest()
    if md5!=ss[2]:
        return None
    return user

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
