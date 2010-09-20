#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
All storage-related class and functions.
'''

import datetime
import random

from google.appengine.ext import db as db

from framework import cache
from framework import ValidationError
from framework import validator

class BaseModel(db.Model):
    '''
    Base model for storage which has basic properties.
    '''
    creation_date = db.DateTimeProperty(required=True, auto_now_add=True)
    modified_date = db.DateTimeProperty(required=True, auto_now=True)

    def __getattr__(self, name):
        if name=='id':
            try:
                return str(self.key())
            except db.NotSavedError:
                return None
        if name.endswith('__raw__'):
            return getattr(self, name[:-7])
        raise AttributeError('\'%s\' object has no attribute \'%s\'' % (self.__class__.__name__, name))

MAX_METADATA = 100

def query_metadata(ref, name=None):
    '''
    Query meta data of specific reference (key of Model).
    
    Args:
        ref: key of owner object.
        name: mata data name, default to None.
    Returns:
        dict contains meta data name-value pairs. If name is not None, all names will return.
    '''
    query = MetaData.all().filter('ref =', ref)
    if name is not None:
        query.filter('name =', name)
    map = {}
    for meta in query.fetch(MAX_METADATA):
        map[str(meta.name)] = meta.value
    return map

def save_metadata(ref, **kw):
    '''
    Save new meta data for specific reference.
    '''
    for name, value in kw:
        MetaData(ref=ref, name=name, value=value).put()

def delete_metadata(ref, names):
    '''
    Delete meta data by names.
    '''
    for meta in MetaData.all().filter('ref =', ref).fetch(MAX_METADATA):
        if str(meta.name) in names:
            meta.delete()

class MetaData(db.Model):
    '''
    Store meta data such as web site, twitter, settings, etc.
    '''
    ref = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    value = db.StringProperty(required=True)

###############################################################################
# User operation
###############################################################################

# role constants:

ROLE_ADMINISTRATOR = 0
ROLE_EDITOR = 10
ROLE_AUTHOR = 20
ROLE_CONTRIBUTOR = 30
ROLE_SUBSCRIBER = 40

ROLES = (ROLE_ADMINISTRATOR, ROLE_EDITOR, ROLE_AUTHOR, ROLE_CONTRIBUTOR, ROLE_SUBSCRIBER)
ROLE_NAMES = ('Administrator', 'Editor', 'Author', 'Contributor', 'Subscriber')

def get_user_by_key(key):
    '''
    Get user by key, or None if not found.
    '''
    return User.get(key)

def get_user_by_email(email):
    '''
    Get user by email, or None if not found.
    '''
    return User.get_by_key_name(email)

def create_user(role, email, password, nicename):
    if role not in ROLES:
        raise ValueError('invalid role.')
    validator.check_email(email)
    validator.check_password(password)

    def tx():
        if User.get_by_key_name(email) is None:
            u = User(key_name=email, role=role, email=email, password=password, nicename=nicename)
            u.put()
            return u
        return None
    user = db.run_in_transaction(tx)
    if user is None:
        raise ValidationError('User create failed.')
    return user

class User(BaseModel):
    '''
    Store a single user
    '''
    role = db.IntegerProperty(required=True, default=ROLE_SUBSCRIBER)
    email = db.EmailProperty(required=True)
    password = db.StringProperty(default='')
    nicename = db.StringProperty(default='')
    locked = db.BooleanProperty(required=True, default=False)

    @staticmethod
    def get_role_name(role):
        '''
        Get role display name by role number.
        
        Args:
            role: role number, constants defined as USER_ROLE_XXX.
        Returns:
            Role name as string.
        '''
        return ROLE_NAMES[role//10]

###############################################################################
# Counter operation
###############################################################################

CACHE_KEY_PREFIX = '_sharded_counter_'

def get_count(name):
    '''
    Retrieve the value for a given sharded counter.
    
    Args:
        name: the name of the counter
    Returns:
        Integer value
    '''
    total = cache.get(CACHE_KEY_PREFIX + name)
    if total is None:
        total = 0
        for counter in ShardedCounter.all().filter('name =', name).fetch(1000):
            total += counter.count
        cache.set(CACHE_KEY_PREFIX + name, str(total))
        return total
    return int(total)

def incr_count(name, delta=1):
    '''
    Increment the value for a given sharded counter.
    
    Args:
        name: the name of the counter
    '''
    config = ShardedCounterConfig.get_or_insert(name, name=name)
    def tx():
        index = random.randint(0, config.shards-1)
        shard_name = name + str(index)
        counter = ShardedCounter.get_by_key_name(shard_name)
        if counter is None:
            counter = ShardedCounter(key_name=shard_name, name=name)
        counter.count += delta
        counter.put()
    db.run_in_transaction(tx)
    cache.incr(CACHE_KEY_PREFIX + name, delta=delta)

def incr_counter_shards(name, num):
    '''
    Increase the number of shards for a given sharded counter.
    Will never decrease the number of shards.
    
    Args:
        name: the name of the counter
        num: how many shards to use
    '''
    config = ShardedCounterConfig.get_or_insert(name, name=name)
    def tx():
        if config.shards < num:
            config.shards = num
            config.put()
    db.run_in_transaction(tx)

class ShardedCounterConfig(db.Model):
    '''
    Tracks the number of shards for each named counter.
    '''
    name = db.StringProperty(required=True)
    shards = db.IntegerProperty(required=True, default=10)

class ShardedCounter(db.Model):
    '''
    Shards for each named counter
    '''
    name = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True, default=0)

###############################################################################
# Setting operation
###############################################################################

DEFAULT_GROUP = '__default__'

def _get_setting(name, group):
    '''
    Get setting object.
    '''
    return Setting.all().filter('name =', name).filter('group =', group).get()

def get_setting(name, group=DEFAULT_GROUP, default_value=None):
    '''
    Get a setting value for specified name and group.
    
    Args:
        name: setting name as string.
        group: setting group as string, default to DEFAULT_GROUP.
        default_value: default value to return if no such setting.
    Returns:
        Setting value as string or unicode.
    '''
    if not isinstance(name, basestring):
        raise ValueError('Name must be basestring.')
    if not isinstance(group, basestring):
        raise ValueError('Group must be basestring.')
    setting = _get_setting(name, group)
    if setting is None:
        return default_value
    return setting.value

def delete_setting(name, group=DEFAULT_GROUP):
    '''
    Delete a setting value for specified name and group.
    
    Args:
        name: setting name as string.
        group: setting group as string, default to DEFAULT_GROUP.
    Returns:
        None
    '''
    if not isinstance(name, basestring):
        raise ValueError('Name must be basestring.')
    if not isinstance(group, basestring):
        raise ValueError('Group must be basestring.')
    setting = _get_setting(name, group)
    if setting is not None:
        setting.delete()

def set_setting(name, value, group=DEFAULT_GROUP):
    '''
    Set new setting for a given name, value and group.
    
    Args:
        name: setting name as string.
        value: setting value as string.
        group: setting group as string, default to DEFAULT_GROUP.
    Returns:
        None
    '''
    if not isinstance(name, basestring):
        raise ValueError('Name must be basestring.')
    if not isinstance(group, basestring):
        raise ValueError('Group must be basestring.')
    if not isinstance(value, basestring):
        raise ValueError('Value must be basestring.')
    setting = _get_setting(name, group)
    if setting is None:
        setting = Setting(name=name, group=group, value=value)
    else:
        setting.value = value
    setting.put()

def get_settings(group=DEFAULT_GROUP):
    '''
    Get settings (100 first) as dict which belongs to specific group.
    
    Args:
        group: setting group as string, default to DEFAULT_GROUP.
    Returns:
        Dict contains key as setting name, value as setting value.
    '''
    if not isinstance(group, basestring):
        raise ValueError('Group must be basestring.')
    settings = Setting.all().filter('group =', group).fetch(100)
    d = {}
    for setting in settings:
        d[str(setting.name)] = setting.value
    return d

class Setting(db.Model):
    '''
    Settings that contains group, name and value.
    '''
    name = db.StringProperty(required=True)
    group = db.StringProperty(required=True, default='__default__')
    value = db.StringProperty()

###############################################################################
# Comment operation
###############################################################################

def get_comment(key):
    '''
    Get a comment by key, or None if not exist.
    '''
    return Comment.get(key)

def get_all_comments(ref):
    '''
    Get all comments by reference key.
    '''
    return Comment.all().filter('ref =', ref).fetch(1000)

def create_comment(ref, email, name, content, ip, approval=True, pending_days=None):
    '''
    Create a comment by given ref, email, name, content, ip, approval and pending_days.
    
    Returns:
        Comment object.
    '''
    validator.check_str(ref, 'ref', False)
    validator.check_email(email)
    validator.check_str(name, 'name', False)
    validator.check_text(content, False)
    pending_time = None
    if not approval and pending_days is not None:
        if pending_days<1 or pending_days>30:
            raise ValueError('Invalid pending time')
        pending_time = datetime.datetime.now() + datetime.timedelta(days=pending_days)
    c = Comment(ref=ref, email=email, name=name, content=content, ip=ip, approval=approval, pending_time=pending_time)
    c.put()
    return c

def approve_comment(key):
    '''
    Approve a comment.
    '''
    c = Comment.get(key)
    if (c is not None) and (not c.approval):
        c.approval = True
        c.put()

def reject_comment(key):
    '''
    Reject a comment. Reject a comment does make it hidden but not delete it.
    '''
    c = Comment.get(key)
    if (c is not None) and c.approval:
        c.approval = False
        c.pending_time = None
        c.put()

def delete_comment(key):
    '''
    Delete a comment by given key.
    '''
    c = Comment.get(key)
    if c is not None:
        c.delete()

def delete_all_comments(ref_key):
    '''
    Delete all comments associated with the reference key. 
    This does not delete all comments immediately from data store. 
    Instead, it add a record in PendingDeleteComment and wait 
    cron job to delete them.
    '''
    p = PendingDeleteComment(ref=ref_key)
    p.put()

def cron_delete_all_comments(ref_key):
    '''
    Delete all comments associated with the reference key. 
    ONLY called by cron job!!!
    '''
    cs = Comment.all().filter('ref =', ref_key).fetch(1000)
    for c in cs:
        c.delete()

class PendingDeleteComment(BaseModel):
    '''
    Store reference key that need to remove comments associated with it.
    '''
    ref = db.StringProperty(required=True)

class Comment(BaseModel):
    '''
    Store a single comment
    '''
    ref = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    ip = db.StringProperty()
    approval = db.BooleanProperty(required=True, default=True)
    pending_time = db.DateTimeProperty()
