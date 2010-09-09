#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
shared.py

all shared db model and related functions.
'''

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

from google.appengine.ext import db

from exweb import context

class Storage(db.Model):
    def __getattr__(self, name):
        if name.endswith('__raw__'):
            return getattr(self, name[:-7])
        raise AttributeError('\'%s\' object has no attribute \'%s\'' % (self.__class__.__name__, name))

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

###############################################################################
# User
###############################################################################

class UserExistError(StandardError):
    pass

# user role constants:

USER_ROLE_ADMINISTRATOR = 0
USER_ROLE_EDITOR = 10
USER_ROLE_AUTHOR = 20
USER_ROLE_CONTRIBUTOR = 30
USER_ROLE_SUBSCRIBER = 40

class User(db.Model):
    'a single user'
    user_role = db.IntegerProperty(required=True, default=USER_ROLE_SUBSCRIBER)
    user_email = db.EmailProperty(required=True)
    user_passwd = db.StringProperty(default='')
    user_nicename = db.StringProperty(default='')
    user_website = db.StringProperty(indexed=False, default='')
    user_registered = db.DateTimeProperty(auto_now_add=True)
    user_locked = db.BooleanProperty(required=True, default=False)

def get_role_name(role):
    '''
    Get role display name by role number.
    
    Args:
        role: role number, constants defined as USER_ROLE_XXX.
    '''
    names = ('Administrator', 'Editor', 'Author', 'Contributor', 'Subscriber')
    return names[role//10]

def get_user_by_email(email):
    '''
    Get user by email.
    
    Args:
        email: email address.
    Return:
        User object or None if no such user.
    '''
    return User.all().filter('user_email =', email).get()

def get_user_by_passwd(email, passwd):
    '''
    Get user by email and password.
    
    Args:
        email: email address.
        passwd: md5-hashed password.
    Returns:
        User object or None if no such user.
    '''
    user = get_user_by_email(email)
    if user and user.user_passwd==passwd:
        return user
    return None

def create_user(role, email, nicename, hashed_passwd='', website=''):
    '''
    Create a new user.
    
    Args:
        role: User role, required.
        email: User email, required.
        nicename: User nicename, required.
        hashed_passwd: User password as md5 hash, or '' if empty. default to ''.
        website: User website. default to ''.
    Returns:
        User object.
    '''
    email = email.strip().lower()
    if get_user_by_email(email) is not None:
        raise UserExistError
    user = User(user_role = role, user_email = email, user_passwd = hashed_passwd, user_nicename = nicename, user_website = website)
    user.put()
    return user

def get_users(role=None):
    if role is None:
        return User.all().order('user_registered').fetch(100)
    return User.all().order('user_registered').filter('user_role =', role).fetch(100)

def lock_user(user_or_key, lock=True):
    '''
    Lock or unlock a User.
    '''
    #FIXME
    pass

###############################################################################
# Setting
###############################################################################

SETTING_GLOBAL = 'global'
SETTING_GLOBAL_DEFAULT_ROLE = 'default-role'

class Setting(db.Model):
    '''
    a single key-value setting grouped by property 'setting_group'
    '''
    setting_group = db.StringProperty(required=True)
    setting_key = db.StringProperty(required=True)
    setting_value = db.StringProperty(indexed=False, default='')

def save_setting(group, key, value):
    '''
    Save a stting's value by its group and key.
    '''
    setting = Setting.all().filter('setting_group =', group).filter('setting_key =', key).get()
    if setting:
        setting.setting_value = value
        setting.put()
    else:
        Setting(setting_group = group, setting_key = key, setting_value = value).put()

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
    setting = Setting.all().filter('setting_group =', group_or_dict).filter('setting_key =', key).get()
    if setting:
        return setting.setting_value
    return default_value

def get_settings(group):
    '''
    get all settings by its group (usually is app's name).
    
    Args:
        group: group of setting.
    Returns:
        a dict (maybe empty) contains key-value pairs, but no group info.
    '''
    settings = Setting.all().filter('setting_group =', group).fetch(1000)
    if not settings:
        return {}
    all = {}
    for setting in settings:
        all[setting.setting_key] = setting.setting_value
    return all

###############################################################################
# Comment
###############################################################################

class Comment(db.Model):
    '''
    Comment on published post, wiki page, photo, etc.
    '''
    reference_key = db.StringProperty(required=True)
    comment_user = db.StringProperty(default='')
    comment_email = db.StringProperty(default='')
    comment_link = db.StringProperty(default='')
    comment_ip = db.StringProperty(required=True)
    comment_date = db.DateTimeProperty(auto_now_add=True)
    comment_content = db.TextProperty(required=True)

def get_comments(ref_target_key, sort_asc=True):
    '''
    Get comments by target object's key.
    
    Args:
        ref_target_key: Target object's key.
        sort_asc: Sort by comment date, the newest first. default to True.
    Returns:
        List of Comment objects.
    '''
    order = sort_asc and 'comment_date' or '-comment_date'
    return Comment.all().filter('reference_key =', ref_target_key).order(order).fetch(1000)

def create_comment(ref_target_key, content, name='', email='', link=''):
    '''
    Create a comment.
    
    Args:
        ref_target_key: Key of target object (post, wiki, photo, etc.).
        content: comment content.
        name: user's name. default to ''.
        email: user's email. default to ''.
        link: user's address. default to ''.
    Returns:
        Created comment object.
    '''
    if context.user is not None:
        name = context.user.user_nicename
        email = context.user.user_email
        link = '/manage/profile/' + str(context.user.key())
    ip = context.request.remote_addr
    content = context.form.get('content')
    c = Comment(reference_key=ref_target_key, comment_user=name, comment_email=email, comment_link=link, comment_ip=ip, comment_content=content)
    c.put()
    return c

def delete_comment(comment_key):
    '''
    Delete a comment by key.
    
    Args:
        comment_key: Key of comment object.
    '''
    c = Comment.get(comment_key)
    if c is not None:
        db.delete(c)

def delete_all_comments_cron(ref_target_key):
    '''
    Delete all comments on the target object by cron. NOTE that this method only make a cron 
    task that will be executed to delete the comments, but not delete them immediately.
    
    Args:
        ref_target_key: Target object's key.
    '''
    # FIXME
    pass
