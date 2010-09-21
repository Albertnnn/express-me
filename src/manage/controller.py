#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Manage app that supports:
  signin: both local (email and password), Google account and OpenID login.
  register: register a local user.
  manage: manage all things of site.
'''

import time
import base64
import hashlib
import logging

from framework import store
from framework import web
from framework.web import get
from framework.web import post

AUTO_SIGNIN_COOKIE = 'auto_signin'

@get('/')
def show_manage(**kw):
    pass

@post('/')
def do_manage(**kw):
    pass

@get('/signin')
def show_signin(**kw):
    ctx = kw['context']
    redirect = ctx.get_argument('redirect', '/')
    return {
            '__view__' : 'signin.html',
            'site' : { 'name' : store.get_setting('name', 'site', 'ExpressMe') },
            'redirect' : redirect,
    }

@get('/register')
def show_register(**kw):
    return {
            '__view__' : 'register.html',
            'error' : '',
            'site' : { 'name' : store.get_setting('name', 'site', 'ExpressMe') },
    }

@post('/register')
def do_register(**kw):
    ctx = kw['context']
    email = ctx.get_argument('email', '').lower()
    password = ctx.get_argument('password')
    nicename = ctx.get_argument('nicename')
    role = int(store.get_setting('default_role', 'site', `store.ROLE_SUBSCRIBER`))
    error = ''
    try:
        user = store.create_user(role, email, password, nicename)
        value = _make_sign_on_cookie(user.id, password, 86400)
        ctx.set_cookie(AUTO_SIGNIN_COOKIE, value)
        return 'redirect:/manage/'
    except store.UserAlreadyExistError:
        error = 'Email is already registered by other'
    except StandardError:
        logging.exception('Error when create user')
        error = 'Unexpected error occurred'
    return {
            '__view__' : 'register.html',
            'error' : error,
            'site' : { 'name' : store.get_setting('name', 'site', 'ExpressMe') },
    }

@post('/signin')
def do_signin(**kw):
    ctx = kw['context']
    redirect = ctx.get_argument('redirect', '/')
    email = ctx.get_argument('email', '').lower()
    password = ctx.get_argument('password')
    user = None
    error = ''
    try:
        user = store.get_user_by_email(email)
        if user is None or user.password!=password:
            error = r'Bad email or password'
    except StandardError, e:
        logging.exception('failed to sign in')
        error = 'Unexpected error occurred: %s' % e.message
    if error:
        return {
                '__view__' : 'signin.html',
                'error' : error,
                'redirect' : redirect,
                'site' : { 'name' : store.get_setting('name', 'site', 'ExpressMe') },
        }
    # make cookie:
    expires = web.COOKIE_EXPIRES_MAX
    try:
        expires = int(ctx.get_argument('expires'))
    except ValueError:
        pass
    value = _make_sign_on_cookie(user.id, password, expires)
    ctx.set_cookie(AUTO_SIGNIN_COOKIE, value, expires)
    return 'redirect:' + redirect

def _make_sign_on_cookie(key, passwd, expire_in_seconds):
    # make sign on cookie with following format:
    # base64(id_expires_md5(id_expires_passwd))
    expires = int(time.time()) + expire_in_seconds
    md5 = hashlib.md5(key + '_' + str(expires) + '_' + passwd).hexdigest()
    return base64.b64encode(key + '_' + str(expires) + '_' + md5)
