#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEPRECATED = True

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Load template by theme
'''

import os

import manage
from manage import shared
import widget

def update_model(rootpath, appname, model):

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

def show_widget(w_instance):
    import logging
    w = w_instance.widget_class()
    id = str(w_instance.key())
    logging.warning('Load ' + id)
    logging.warning('Model = ' + str(w_instance.model))
    w.load(id, w_instance.model)
    return w.render()
