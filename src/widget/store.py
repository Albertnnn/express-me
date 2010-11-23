#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

DEPRECATED = True

from google.appengine.ext import db

DEFAULT_GROUP = 'default'

def get_instance_settings_as_dict(widget_instance):
    '''
    get widget instance settings as dict which contains key-value pairs (both str/unicode).
    
    Args:
        widget_instance: WidgetInstance object.
    Returns:
        Settings as dict which both key and value are str/unicode.
    '''
    list = WidgetInstanceSetting.all().filter('widget_instance ==', widget_instance).fetch(100)
    d = {}
    for setting in list:
        d[setting.setting_key] = setting.setting_value
    import logging
    logging.info('get_instance_settings_as_dict: ' + str(d))
    return d

def update_instance_settings(widget_instance, setting_as_dict):
    '''
    Update instance settings.
    
    Args:
      widget_instance: WidgetInstance object.
      setting_as_dict: new settings as dict contains key as str and value as str or unicde.
    Returns:
      None
    '''
    group = widget_instance.widget_group
    db.delete(get_instance_settings(widget_instance))
    for name, value in setting_as_dict.items():
        WidgetInstanceSetting(
                widget_group=group,
                widget_instance=widget_instance,
                setting_name=name,
                setting_value=value
        ).put()
