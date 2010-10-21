#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Model for manage app.
'''

import random
import hashlib
from datetime import datetime
from datetime import timedelta

from google.appengine.ext import db
from framework import store

TOKEN_EXPIRED_TIMEDELTA = timedelta(2, 0)

class ResetPasswordToken(store.BaseModel):
    '''
    Store Reset-Password token.
    '''
    ref = db.StringProperty(required=True)
    token = db.StringProperty(required=True)

    def is_expired(self):
        delta = datetime.now() - self.creation_date
        return delta > TOKEN_EXPIRED_TIMEDELTA

def cron_delete_expired_token():
    '''
    Called by cron task. Delete all expired token.
    '''
    exp = datetime.now() - TOKEN_EXPIRED_TIMEDELTA
    ts = ResetPasswordToken.all().filter('creation_date <', exp).fetch(200)
    for t in ts:
        t.delete()

def get_reset_password_token(user_key):
    '''
    Get the latest token by given user.
    
    Args:
        user_key: user's key.
    Returns:
        Token as string, or None if no valid token.
    '''
    t = ResetPasswordToken.all().filter('ref =', user_key).order('-creation_date').get()
    if t is not None and not t.is_expired():
        return t.token
    return None

def create_reset_password_token(user_key):
    '''
    Create a new token for reseting password.
    
    Args:
        user_key: user's key.
    Returns:
        Token as string.
    '''
    token = _generate_token(user_key)
    ResetPasswordToken(ref=user_key, token=token).put()
    return token

def _generate_token(user_key):
    '''
    Generate token.
    '''
    s = '%s, %d, %s' % (str(datetime.now()), random.randint(1000000, 10000000), user_key)
    return hashlib.md5(s).hexdigest()
