#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Load template by theme
'''

import os

from exweb import context

import manage
from manage import shared
import widget

def load_template(selected=None):
    '''
    Load template and return its path.
    '''
    themes = manage.get_themes()
    if selected is None:
        selected = shared.get_setting('theme', 'selected', '')
    if not selected in themes:
        selected = themes[0]
    return ('theme', selected, 'template.html')

def update_model(rootpath, appname, model):
    model['site'] = {
            'title' : shared.get_setting('global', 'site_title', 'ExpressMe'),
            'subtitle' : shared.get_setting('global', 'site_subtitle', 'powered by ExpressMe')
    }
    model['navigations'] = manage.get_navigations()
    model['user'] = context.user
    model['app'] = appname
    # set current theme = 'simple':
    theme = shared.get_setting('theme', 'selected', '')
    if not theme:
        themes = manage.get_themes()
        theme = themes[0]
        shared.save_setting('theme', 'selected', theme)
    model['theme'] = theme
    # add widgets:
    instances = widget.get_widget_instances()
    all_settings = widget.get_all_instances_settings()
    widget.bind_instance_model(instances, all_settings)
    import logging
    model['widgets'] = instances
    model['show_widget__raw__'] = show_widget
    logging.warning('loaded ' + str(instances))

    # set app_main to path:
    app_main = os.path.join(rootpath, 'theme', theme, appname + '.main.html')
    if not os.path.exists(app_main):
        app_main = os.path.join(rootpath, appname, 'main.html')
    model['app_main'] = app_main
    model['format_datetime'] = lambda d : d.strftime('%Y-%m-%d %H:%M:%S')
    model['format_date'] = lambda d : d.strftime('%Y-%m-%d')
    model['format_time'] = lambda d : d.strftime('%H:%M:%S')

def show_widget(w_instance):
    import logging
    w = w_instance.widget_class()
    id = str(w_instance.key())
    logging.warning('Load ' + id)
    logging.warning('Model = ' + str(w_instance.model))
    w.load(id, w_instance.model)
    return w.render()
