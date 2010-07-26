#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Filter for auto-signon and bind user to context.
'''

from exweb import context
import manage

def auto_sign_on_filter():
    context.user = None
    value = context.get_cookie(manage.COOKIE_AUTO_SIGN_ON)
    if value:
        user = manage.validate_sign_on_cookie(value, manage.get_user)
        if user:
            context.user = user
            return
        else:
            context.remove_cookie(manage.COOKIE_AUTO_SIGN_ON)
    # try google sign on:
    try:
        from google.appengine.api import users
        gu = users.get_current_user()
        if gu:
            context.user = manage.shared.get_user_by_email(gu.email())
    except ImportError:
        pass
