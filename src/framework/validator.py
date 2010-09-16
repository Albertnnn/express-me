#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Validator API.
'''

import types
import re

REGEX_EMAIL = re.compile(r'^[a-z0-9\.\_\-]+\@([a-z0-9\-]+\.){1,3}[a-z]{2,6}$')
REGEX_MD5 = re.compile(r'^[a-f0-9]{32}$')

def check_email(email):
    '''
    Check email if it is validated.
    
    Args:
        email: email address for test.
    Raises:
        ValueError if not a valid email.
    '''
    check_str(email, 'email')
    if REGEX_EMAIL.match(email) is None:
        raise ValueError('%s is not an email' % email)

def check_str(str, name='argument'):
    '''
    Check if it is a string.
    
    Args:
        str: object for test.
    Raises:
        ValueError if not a string.
    '''
    if not isinstance(str, types.StringTypes):
        raise ValueError('%s is not a string' % name)

def check_password(password, allow_empty=True):
    '''
    Check password if it is validated.
    
    Args:
        password: password for test.
        allow_empty: true if skip empty password.
    Raises:
        ValueError if not a valid password.
    '''
    check_str(password, 'password')
    if (not allow_empty) and password and (REGEX_MD5.match(password) is None):
        raise ValueError('%s is not a password' % password)
