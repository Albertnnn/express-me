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
import urllib

from framework import ApplicationError
from framework import store
from framework import web
from framework import mail
from framework import recaptcha
from framework.web import get
from framework.web import post

from manage import model

AUTO_SIGNIN_COOKIE = 'auto_signin'

def _get_site_info():
    return { 'name' : store.get_setting('name', 'site', 'ExpressMe') }

@get('/')
def show_manage(**kw):
    pass

@post('/')
def do_manage(**kw):
    pass

@get('/forgot')
def show_forgot():
    return {
            '__view__' : 'forgot.html',
            'email' : '',
            'error' : '',
            'recaptcha_public_key' : recaptcha.get_public_key(),
            'site' : _get_site_info(),
    }

@post('/forgot')
def do_forgot(**kw):
    ip = kw['request'].remote_addr
    ctx = kw['context']
    # verify captcha:
    challenge = ctx.get_argument('recaptcha_challenge_field', '')
    response = ctx.get_argument('recaptcha_response_field', '')
    email = ctx.get_argument('email', '')
    user = store.get_user_by_email(email)
    if user is None:
        return {
            '__view__' : 'forgot.html',
            'email' : email,
            'error' : 'Email is not exist',
            'recaptcha_public_key' : recaptcha.get_public_key(),
            'site' : _get_site_info(),
        }
    result, error = recaptcha.verify_captcha(challenge, response, recaptcha.get_private_key(), ip)
    if result:
        token = model.create_reset_password_token(user.id)
        sender = store.get_setting('sender', 'mail', '')
        if not sender:
            raise ApplicationError('Cannot send mail: mail sender address is not configured.')
        appid = kw['environ']['APPLICATION_ID']
        body = r'''Dear %s
  You received this mail because you have requested reset your password.
  Please paste the following link to the address bar of the browser, then press ENTER:
  https://%s.appspot.com/manage/reset?token=%s
''' % (user.nicename, appid, token)
        html = r'''<html>
<body>
<p>Dear %s</p>
<p>You received this mail because you have requested reset your password.<p>
<p>Please paste the following link to reset your password:</p>
<p><a href="https://%s.appspot.com/manage/reset?token=%s">https://%s.appspot.com/manage/reset?token=%s</a></p>
<p>If you have trouble in clicking the URL above, please paste the following link to the address bar of the browser, then press ENTER:</p>
<p>https://%s.appspot.com/manage/reset?token=%s</p>
</body>
</html>
''' % (urllib.quote(user.nicename), appid, token, appid, token, appid, token)
        mail.send(sender, email, 'Reset your password', body, html)
        return {
            '__view__' : 'sent.html',
            'email' : email,
            'site' : _get_site_info(),
    }
    return {
            '__view__' : 'forgot.html',
            'email' : email,
            'error' : error,
            'recaptcha_public_key' : recaptcha.get_public_key(),
            'site' : _get_site_info(),
    }

@get('/g_signin')
def do_google_signin(**kw):
    ctx = kw['context']
    # get google user:
    from google.appengine.api import users
    gu = users.get_current_user()
    if not gu:
        logging.error('Google account info is not found. Exit g_signin...')
        raise ApplicationError('Cannot find user information')
    ctx.delete_cookie(AUTO_SIGNIN_COOKIE)
    email = gu.email().lower()
    nicename = gu.nickname()
    # check if user exist:
    user = store.get_user_by_email(email)
    if user is None:
        # auto-create new user:
        role = store.ROLE_SUBSCRIBER
        if users.is_current_user_admin():
            role = store.ROLE_ADMINISTRATOR
        user = store.create_user(role, email, '', nicename)
    redirect = ctx.get_argument('redirect', '/')
    logging.info('Sign in successfully with Google account and redirect to %s...' % redirect)
    return 'redirect:%s' % redirect

@get('/signin')
def show_signin(**kw):
    ctx = kw['context']
    redirect = ctx.get_argument('redirect', '/')
    google_signin_url = None
    try:
        from google.appengine.api import users
        google_signin_url = users.create_login_url('/manage/g_signin?redirect=' + urllib.quote(redirect))
    except ImportError:
        pass
    return {
            '__view__' : 'signin.html',
            'error' : '',
            'redirect' : redirect,
            'google_signin_url' : google_signin_url,
            'site' : _get_site_info(),
    }

@get('/register')
def show_register(**kw):
    return {
            '__view__' : 'register.html',
            'error' : '',
            'site' : _get_site_info(),
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
            'site' : _get_site_info(),
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
                'site' : _get_site_info(),
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
