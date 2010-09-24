#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Global interceptors for ExpressMe application.
'''

from manage import cookie
from framework import store

def intercept(kw):
    _detect_current_user(kw)

def _detect_current_user(kw):
    kw['current_user'] = None
    ctx = kw['context']
    auto_signin_cookie = ctx.get_cookie(cookie.AUTO_SIGNIN_COOKIE)
    if auto_signin_cookie:
        user = cookie.validate_sign_in_cookie(auto_signin_cookie, store.get_user_by_key)
        if user:
            kw['current_user'] = user
