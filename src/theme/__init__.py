#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Theme for apps.
'''

import os
import logging

from framework import view
import navigation
import siteconfig
import runtime

def get_themes(use_cache=True):
    '''
    Get all themes' logic names.
    
    Returns:
        list of themes' logic names.
    '''
    theme_root = os.path.dirname(__file__)
    theme_dirs = os.listdir(theme_root)
    return [t for t in theme_dirs if os.path.isfile(os.path.join(theme_root, t, 'template.html'))]

def get_theme():
    '''
    Get default theme
    '''
    th = 'default'
    return th

def render(appname, app_model, **kw):
    '''
    Render model with theme.
    '''
    th = get_theme()
    logging.info('render using theme "%s"...' % th)
    # load widget:
    # TODO...
    # prepare model for theme:
    site = siteconfig.get_site_settings()
    tz = site.get_tzinfo()
    utils = runtime.get_runtime_utils(tz, str(site.date_format), str(site.time_format))
    app_model['utils'] = utils
    app_model['user'] = kw['current_user']
    app_model['site'] = site
    embedded_app = view.render(appname, app_model)
    title = site.title
    app_title = app_model.get('__title__', None)
    if app_title:
        title = app_title + ' - ' + title
    model = {
            '__view__' : 'template',
            '__app__' : embedded_app,
            '__header__' : app_model.get('__header__', ''),
            '__footer__' : app_model.get('__footer__', ''),
            'utils' : utils,
            'app' : appname,
            'user' : kw['current_user'],
            'title' : title,
            'site' : site,
            'navigations' : navigation.get_navigation(),
    }
    return view.render('theme', model, view_dir=th)
