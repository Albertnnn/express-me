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

def get_themes():
    '''
    Get all themes' logic names.
    
    Returns:
        list of themes' logic names.
    '''
    theme_root = os.path.dirname(__file__)
    view_root = os.path.join(theme_root, 'view')
    all_files = os.listdir(view_root)
    themes = [f for f in all_files if f.endswith('.html') and os.path.isfile(os.path.join(view_root, f))]
    return [f[:-5] for f in themes]

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
    embedded_app = view.render(appname, app_model)
    title = site.title
    app_title = app_model.get('__title__', None)
    if app_title:
        title = app_title + ' - ' + title
    model = {
            '__view__' : th,
            '__app__' : embedded_app,
            'utils' : utils,
            'app' : appname,
            'user' : kw['current_user'],
            'title' : title,
            'site' : site,
            'navigations' : navigation.get_navigation(),
    }
    return view.render('theme', model)
