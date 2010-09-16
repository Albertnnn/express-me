#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Simple API for user operations.
'''

from google.appengine.ext import db as db

from framework import store
from framework import validator

# user role constants:

USER_ROLE_ADMINISTRATOR = 0
USER_ROLE_EDITOR = 10
USER_ROLE_AUTHOR = 20
USER_ROLE_CONTRIBUTOR = 30
USER_ROLE_SUBSCRIBER = 40

ROLES = (USER_ROLE_ADMINISTRATOR, USER_ROLE_EDITOR, USER_ROLE_AUTHOR, USER_ROLE_CONTRIBUTOR, USER_ROLE_SUBSCRIBER)
ROLE_NAMES = ('Administrator', 'Editor', 'Author', 'Contributor', 'Subscriber')

def create(role, email, password, nicename):
    if role not in ROLES:
        raise ValueError('invalid role.')
    validator.check_email(email)
    validator.check_password(password)

    def tx():
        if User.get_by_key_name(email) is None:
            return User.get_or_insert(email, role=role, email=email.lower(), password=password)
        return None
    user = db.run_in_transaction(tx)
    if user is None:
        raise store.StoreError('User create failed.')
    return user

class User(store.BaseModel):
    '''
    Store a single user
    '''
    role = db.IntegerProperty(required=True, default=USER_ROLE_SUBSCRIBER)
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
