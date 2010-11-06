#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import os

from google.appengine.ext import db

from framework import store
from framework import cache

def get_installed_widgets():
    '''
    Get installed widgets as dict containing key=package_name, value=class object.
    '''
    installed_path = os.path.join(os.path.split(__file__)[0], 'installed')
    packages = os.listdir(installed_path)
    valid_packages = [pkg for pkg in packages if os.path.isfile(os.path.join(installed_path, pkg, '__init__.py'))]
    d = {}
    for pkg_name in valid_packages:
        cls = __import__('widget.installed.%s' % pkg_name, fromlist=['Widget']).Widget
        d[pkg_name] = cls
    return d

def load_widget_class(name):
    return __import__('widget.installed.%s' % name, fromlist='Widget').Widget

DEFAULT_COLUMN = 0

class WidgetInstance(db.Model):
    '''
    Store widget instance that can display in a widget bar.
    
    A widget instance has 3 properties:
    
    column: index (0-9) of the widget column that this widget belongs to. Default to DEFAULT_COLUMN (0).
    name: the widget module name.
    display_order: the widget display order.
    '''
    column = db.IntegerProperty(required=True, default=DEFAULT_COLUMN)
    name = db.StringProperty(required=True)
    display_order = db.IntegerProperty(required=True)

    def __str__(self):
        return 'WidgetInstance(name=%s)' % self.name

    __repr__ = __str__

def get_instances(column, use_cache=True):
    '''
    Get widget instances of the given column.
    
    Args:
      column: index of the column, 0-9.
      use_cache: True if fetch from cache first. Default to True.
    Returns:
      List of widget instances, as well as settings attached with each widget instance.
    '''
    def _load():
        instances = WidgetInstance.all().filter('column =', column).order('display_order')
        for instance in instances:
            instance.settings = get_instance_settings(instance)
        return instances
    if use_cache:
        return cache.get('__widget_column_%s__' % column, _load)
    return _load()

def get_instance_settings(widget_instance):
    '''
    Get widget instance settings.
    
    Args:
      Widget instance object.
    
    Return:
      Dict (name=value) as settings of WidgetInstance.
    '''
    return store.get_settings('widget_instance_%s' % widget_instance.id)

def save_instance_settings(widget_instance, setting_as_dict):
    '''
    Update instance settings.
    
    Args:
      widget_instance: WidgetInstance object.
      setting_as_dict: new settings as dict contains key as str and value as str or unicde.
    Returns:
      None
    '''
    group = 'widget_instance_%s' % widget_instance.id
    store.delete_settings(group)
    for k, v in setting_as_dict.items():
        store.set_setting(k, v, group)

def delete_widget_instance(key):
    '''
    Delete a Widget instance and all its settings.
    
    Args:
      key: Widget instance key.
    Returns:
      None
    '''
    instance = WidgetInstance.get(key)
    if instance is not None:
        instance.delete()
        store.delete_settings('widget_instance_%s' % key)
