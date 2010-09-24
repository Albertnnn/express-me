#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Manage cookie for auto-signin.
'''

import time
import base64
import hashlib

AUTO_SIGNIN_COOKIE = 'auto_signin'

def make_sign_in_cookie(key, passwd, expire_in_seconds):
    # make sign in cookie with following format:
    # base64(id_expires_md5(id_expires_passwd))
    id = str(key)
    expires = str(int(time.time()) + expire_in_seconds)
    md5 = hashlib.md5(','.join([id, expires, passwd])).hexdigest()
    return base64.b64encode(','.join([id, expires, md5]))

def validate_sign_in_cookie(value, get_user):
    '''
    Validate sign in cookie.
    
    Args:
        value: cookie value, a base64-encoded string.
        get_user: function for get User object by key.
    
    Returns:
        User object if sign in ok, None if cookie is invalid.
    '''
    dec = base64.b64decode(str(value))
    ss = dec.split(',')
    # ss = [key, expires, md5]
    if len(ss)!=3:
        return None
    key = ss[0]
    expires = ss[1]
    md5 = ss[2]
    try:
        if float(expires)<time():
            return None
    except ValueError:
        return None
    user = get_user(key)
    if user is None:
        return None
    calc_md5 = hashlib.md5(','.join([key, expires, str(user.user_passwd)])).hexdigest()
    if calc_md5!=md5:
        return None
    return user
