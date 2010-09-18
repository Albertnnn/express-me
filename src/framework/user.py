#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Simple API for user operations.
'''

from google.appengine.ext import db as db

from framework import ValidationError
from framework import store
from framework import validator

# user role constants:

ROLE_ADMINISTRATOR = 0
ROLE_EDITOR = 10
ROLE_AUTHOR = 20
ROLE_CONTRIBUTOR = 30
ROLE_SUBSCRIBER = 40

ROLES = (ROLE_ADMINISTRATOR, ROLE_EDITOR, ROLE_AUTHOR, ROLE_CONTRIBUTOR, ROLE_SUBSCRIBER)
ROLE_NAMES = ('Administrator', 'Editor', 'Author', 'Contributor', 'Subscriber')

def get_by_key(key):
    '''
    Get user by key, or None if not found.
    '''
    return User.get(key)

def get_by_email(email):
    '''
    Get user by email, or None if not found.
    '''
    return User.get_by_key_name(email)

def create(role, email, password, nicename):
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

class User(store.BaseModel):
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
