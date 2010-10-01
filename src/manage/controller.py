#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Manage app that supports:
  signin: both local (email and password), Google account and OpenID login.
  register: register a local user.
  manage: manage all things of site.
'''

import logging
import urllib

from google.appengine.api import users

from framework import ApplicationError
from framework import store
from framework import web
from framework import mail
from framework import view
from framework import recaptcha
from framework.web import get
from framework.web import post
from framework.web import mapping

from manage import PermissionError
from manage import model
from manage import cookie

from manage.common import AppMenu

import appconfig
from version import get_version

_MODEL_UTILS = {
        'format_datetime' : lambda d : d.strftime('%Y-%m-%d %H:%M:%S'),
        'format_date' : lambda d : d.strftime('%Y-%m-%d'),
        'format_time' : lambda d : d.strftime('%H:%M:%S'),
}

def _get_site_info():
    return { 'name' : store.get_setting('name', 'site', 'ExpressMe') }

@mapping('/')
def do_manage(**kw):
    current_user = kw['current_user']
    if current_user is None:
        return 'redirect:/manage/signin?redirect=%s/manage/' % kw['request'].host_url
    ctx = kw['context']
    role = current_user.role
    app = ctx.get_argument('app', 'manage')
    command = ctx.get_argument('command', 'profile')
    menus = []
    selected_menu = None
    selected_menu_item = None
    for appname in appconfig.apps:
        logging.info('Import %s.appmanage...' % appname)
        app_mod = __import__(appname, fromlist=['appmanage']).appmanage
        for m in app_mod.get_menus():
            fm = _filter_menu(m, role, appname)
            if fm is not None:
                menus.append(fm)
                if appname==app:
                    for item in fm.items:
                        if item.command==command:
                            selected_menu_item = item
                            selected_menu = fm
                            break
    # check permission:
    if selected_menu_item is None or selected_menu_item.role < current_user.role:
        raise PermissionError('You do not have permission to access this resource.')
    model = {
            'user' : current_user,
            'app' : app,
            'command' : command,
            'menus' : menus,
            'selected_menu' : selected_menu,
            'selected_menu_item' : selected_menu_item,
            'version' : get_version(),
    }
    req = kw['request']
    embed_context = web.Context()
    embed_context.method = req.method.lower()
    embed_context.get_argument = lambda argument_name, default_value=None: req.get(argument_name, default_value)
    embed_context.get_arguments = lambda argument_name: req.get_all(argument_name)
    embed_context.arguments = lambda: req.arguments()
    app_mod = __import__(appname, fromlist=['appmanage']).appmanage
    # call app's manage method and get the embed model:
    embed_model = app_mod.manage(current_user, app, command, embed_context)
    embed_model['app'] = app
    embed_model['command'] = command
    embed_model['user'] = current_user
    embed_model['utils'] = _MODEL_UTILS
    embeded = view.render(app, embed_model)
    # copy some value from embed_model:
    for key in ['info', 'warning', 'error']:
        if key in embed_model:
            model[key] = embed_model[key]
    model['__embeded__'] = embeded
    model['__view__'] = 'manage'
    return model

def _filter_menu(menu, role, appname):
    '''
    Check AppMenu and return a authorized menu.
    
    Args:
        menu: AppMenu object.
        role: role of current user.
    Returns:
        new AppMenu object that has authority to the menu, or None if all items are forbidden.
    '''
    m = AppMenu(menu.title)
    m.app = appname
    for item in menu.items:
        if item.role >= role:
            item.app = appname
            m.items.append(item)
    if m.items:
        return m
    return None

@get('/forgot')
def show_forgot():
    return {
            '__view__' : 'forgot',
            'email' : '',
            'error' : '',
            'recaptcha_public_key' : recaptcha.get_public_key(),
            'site' : _get_site_info(),
            'version' : get_version(),
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
            '__view__' : 'forgot',
            'email' : email,
            'error' : 'Email is not exist',
            'recaptcha_public_key' : recaptcha.get_public_key(),
            'site' : _get_site_info(),
            'version' : get_version(),
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
            '__view__' : 'sent',
            'email' : email,
            'site' : _get_site_info(),
            'version' : get_version(),
    }
    return {
            '__view__' : 'forgot',
            'email' : email,
            'error' : error,
            'recaptcha_public_key' : recaptcha.get_public_key(),
            'site' : _get_site_info(),
            'version' : get_version(),
    }

@get('/g_signin')
def do_google_signin(**kw):
    ctx = kw['context']
    # get google user:
    gu = users.get_current_user()
    if gu is None:
        logging.error('Google account info is not found. Exit g_signin...')
        raise ApplicationError('Cannot find user information')
    ctx.delete_cookie(cookie.AUTO_SIGNIN_COOKIE)
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
    elif users.is_current_user_admin() and user.role!=store.ROLE_ADMINISTRATOR:
        user.role = store.ROLE_ADMINISTRATOR
        user.put()
    ctx.set_cookie(cookie.IS_FROM_GOOGLE_COOKIE, 'yes', 31536000)
    redirect = ctx.get_argument('redirect', '/')
    logging.info('Sign in successfully with Google account and redirect to %s...' % redirect)
    return 'redirect:%s' % redirect

@mapping('/signout')
def signout(**kw):
    ctx = kw['context']
    ctx.delete_cookie(cookie.AUTO_SIGNIN_COOKIE)
    redirect = '/'
    referer = kw['request'].headers.get('Referer')
    if referer and referer.find('/manage/signout')==(-1):
        redirect = referer
    if ctx.get_cookie(cookie.IS_FROM_GOOGLE_COOKIE)=='yes':
        ctx.delete_cookie(cookie.IS_FROM_GOOGLE_COOKIE)
        redirect = users.create_logout_url(redirect)
    return 'redirect:%s' % redirect

@get('/register')
def show_register(**kw):
    return {
            '__view__' : 'register',
            'error' : '',
            'site' : _get_site_info(),
            'version' : get_version(),
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
        value = cookie.make_sign_in_cookie(user.id, password, 86400)
        ctx.set_cookie(cookie.AUTO_SIGNIN_COOKIE, value)
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
            'version' : get_version(),
    }

def _get_google_signin_url(redirect):
    return users.create_login_url(redirect)

@get('/signin')
def show_signin(**kw):
    ctx = kw['context']
    redirect = ctx.get_argument('redirect', '/')
    google_signin_url = _get_google_signin_url('/manage/g_signin?redirect=' + urllib.quote(redirect))
    return {
            '__view__' : 'signin',
            'error' : '',
            'redirect' : redirect,
            'google_signin_url' : google_signin_url,
            'site' : _get_site_info(),
            'version' : get_version(),
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
                '__view__' : 'signin',
                'error' : error,
                'redirect' : redirect,
                'site' : _get_site_info(),
                'version' : get_version(),
                'google_signin_url' : _get_google_signin_url('/manage/g_signin?redirect=' + urllib.quote(redirect)),
        }
    # make cookie:
    expires = web.COOKIE_EXPIRES_MAX
    try:
        expires = int(ctx.get_argument('expires'))
    except ValueError:
        pass
    value = cookie.make_sign_in_cookie(user.id, password, expires)
    ctx.set_cookie(cookie.AUTO_SIGNIN_COOKIE, value, expires)
    return 'redirect:' + redirect
