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

class AppMenu(object):
    def __init__(self, title):
        self.title = title

class AppMenuItem(object):
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

# empty password:
EMPTY_PASSWORD = '________________________________'

# user role constants:

USER_ROLE_ADMINISTRATOR = 0
USER_ROLE_EDITOR = 10
USER_ROLE_AUTHOR = 20
USER_ROLE_CONTRIBUTOR = 30
USER_ROLE_SUBSCRIBER = 40

def get_role_name(role):
    names = ('Administrator', 'Editor', 'Author', 'Contributor', 'Subscriber')
    return names[role//10]

class UserExistError(StandardError):
    pass

class User(db.Model):
    'a single user'
    user_role = db.IntegerProperty(required=True, default=USER_ROLE_SUBSCRIBER)
    user_email = db.EmailProperty(required=True)
    user_passwd = db.StringProperty(required=True)
    user_nicename = db.StringProperty(default='')
    user_website = db.StringProperty(indexed=False, default='')
    user_registered = db.DateTimeProperty(auto_now_add=True)
    user_locked = db.BooleanProperty(required=True, default=False)

class Setting(db.Model):
    '''
    a single key-value setting grouped by property 'setting_group'
    '''
    setting_group = db.StringProperty(required=True)
    setting_key = db.StringProperty(required=True)
    setting_value = db.StringProperty(indexed=False, default='')

class Comment(db.Model):
    '''
    Comment on published post, wiki page, photo, etc.
    '''
    reference_key = db.StringProperty(required=True)
    comment_user = db.StringProperty(default='')
    comment_link = db.StringProperty(default='')
    comment_ip = db.StringProperty(required=True)
    comment_date = db.DateTimeProperty(auto_now_add=True)
    comment_content = db.TextProperty(required=True)

def create_comment(ref_target_key, content, name='', link=''):
    user = 'Guest' # anomymouse user
    if name:
        user = name
    if context.user is not None:
        user = context.user.user_nicename
        link = '/manage/profile/' + str(context.user.key())
    ip = context.request.remote_addr
    content = context.form.get('content')
    c = Comment(reference_key=ref_target_key, comment_user=user, comment_link=link, comment_ip=ip, comment_content=content)
    c.put()
    return c

def get_comments(key, sort_asc=True):
    order = sort_asc and 'comment_date' or '-comment_date'
    return Comment.all().filter('reference_key =', key).order(order).fetch(1000)

def delete_comment(comment_key):
    c = Comment.get(comment_key)
    if c is not None:
        db.delete(c)

def delete_all_comments(ref_key):
    db.delete(get_comments(ref_key))

# cookie constants:

COOKIE_AUTO_SIGN_ON = '_auto_signon_'
COOKIE_EXPIRES_MIN = 86400
COOKIE_EXPIRES_MAX = 31536000

SETTING_GLOBAL = 'global'
SETTING_GLOBAL_DEFAULT_ROLE = 'default-role'

def save_setting(group, key, value):
    '''
    Save a stting's value by its group and key.
    '''
    settings = Setting.all().filter('setting_group =', group).filter('setting_key =', key).fetch(1)
    if settings:
        settings[0].setting_value = value
        settings[0].put()
    else:
        s = Setting(setting_group = group, setting_key = key, setting_value = value)
        s.put()

def get_setting(group_or_dict, key, default_value=''):
    '''
    get a setting's value by its group (usually is app name) and key.
    
    Args:
        group_or_dict: setting group as string, or dict.
        key: key of setting.
        default_value: if not found, default_value will returned, default to ''.
    Returns:
        setting value.
    '''
    if isinstance(group_or_dict, dict):
        if key in group_or_dict:
            return group_or_dict[key]
        return default_value
    settings = Setting.all().filter('setting_group =', group_or_dict).filter('setting_key =', key).fetch(1)
    if settings:
        return settings[0].setting_value
    return default_value

def get_settings(group):
    '''
    get all settings by its group (usually is app name).
    
    Args:
        group: group of setting.
    Returns:
        a dict (maybe empty) contains key-value pairs.
    '''
    settings = Setting.all().filter('setting_group =', group).fetch(1000)
    if not settings:
        return {}
    all = {}
    for setting in settings:
        all[setting.setting_key] = setting.setting_value
    return all

NAV_MAX = 10

def get_navigations():
    '''
    Get navigation definitions with [(title, url), (...), ...].
    
    Returns:
        A list contains multiple tuple of (title, url).
    '''
    navs = get_settings('navigation')
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

def create_user(role, email, hashed_passwd, nicename, website):
    '''
    Create a new user.
    
    Returns:
        User object.
    '''
    email = email.strip().lower()
    if is_user_exist(email):
        raise UserExistError
    user = User(user_role = role, user_email = email, user_passwd = hashed_passwd, user_nicename = nicename, user_website = website)
    user.put()
    return user

def get_users(role=None):
    if role is None:
        return User.all().order('user_registered').fetch(100)
    return User.all().order('user_registered').filter('user_role =', role).fetch(100)

def is_user_exist(email):
    return User.all().filter('user_email =', email).fetch(1)

def get_user_by_email(email):
    '''
    Get user by email.
    
    Args:
        email: email address.
    Return:
        User object or None if no such user.
    '''
    users = User.all().filter('user_email =', email).fetch(1)
    if users:
        return users[0]
    return None

def get_user(key):
    '''
    Get User object by key.
    
    Args:
        key: key as string.
    
    Returns:
        User object or None if not found.
    '''
    return User.get(key)

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
