#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import os
import copy

from google.appengine.ext import db

from framework import store
from framework import cache

from widget import WidgetSetting

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

def get_default_settings(widget_class):
    d = {}
    return d

def load_widget_class(name):
    return __import__('widget.installed.%s' % name, fromlist='Widget').Widget

class WidgetInstance(store.BaseModel):
    '''
    Store widget instance that can display in a widget bar.
    
    A widget instance has 3 properties:
    
    sidebar: index (0-9) of the sidebar that this widget belongs to. Default to 0.
    name: the widget module name (or widget id).
    display_order: the widget display order.
    '''
    name = db.StringProperty(required=True)
    sidebar = db.IntegerProperty(required=True, default=0)
    display_order = db.IntegerProperty(required=True)

    def __str__(self):
        return 'WidgetInstance(name=%s, sidebar=%s, display_order=%s)' % (self.name, self.sidebar, self.display_order)

    __repr__ = __str__

def create_widget_instance(name, sidebar):
    '''
    Create a new widget instance.
    
    Returns:
      The created WidgetInstance object.
    '''
    count = WidgetInstance.all().filter('sidebar =', sidebar).count(101)
    if count>=100:
        raise StandardError('Maximum widgets exceeded in a sidebar.')
    w = WidgetInstance(name=name, sidebar=sidebar, display_order=count)
    w.put()
    return w

def get_widget_instances(sidebar, use_cache=True):
    '''
    Get widget instances of the given sidebar.
    
    Args:
      sidebar: index of the sidebar, 0-9.
      use_cache: True if fetch from cache first. Default to True.
    Returns:
      List of widget instances, as well as settings attached with each widget instance.
    '''
    def _load():
        instances = WidgetInstance.all().filter('sidebar =', sidebar).order('display_order').fetch(100)
        widgets = get_installed_widgets()
        for instance in instances:
            if instance.name in widgets:
                instance.settings = get_widget_instance_settings(instance, widgets[instance.name])
        return instances
    if use_cache:
        return cache.get('__widget_sidebar_%s__' % sidebar, _load)
    return _load()

def get_widget_instance_settings(widget_instance, widget_class):
    '''
    Get widget instance settings.
    
    Args:
      widget_instance: Widget instance object.
      widget_class: Widget class object.
    
    Return:
      Dict (name=value) as settings of WidgetInstance.
    '''
    d = store.get_settings('widget_instance_%s' % widget_instance.id)
    settings = get_widget_class_settings(widget_class)
    
    return d

def save_widget_instance_settings(instance, setting_as_dict):
    '''
    Update instance settings.
    
    Args:
      instance: WidgetInstance object.
      setting_as_dict: new settings as dict contains key as str and value as str or unicde.
    Returns:
      None
    '''
    group = 'widget_instance_%s' % instance.id
    cache.delete('__widget_sidebar_%s__' % instance.sidebar)
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
        cache.delete('__widget_sidebar_%s__' % instance.sidebar)
        instance.delete()
        store.delete_settings('widget_instance_%s' % key)

def get_widget_class_settings(widget_class):
    '''
    Get widget class settings.
    
    Args:
      Widget class.
    
    Return:
      List contains WidgetSetting object.
    '''
    attrs = [getattr(widget_class, attr) for attr in dir(widget_class)]
    return [copy.copy(attr) for attr in attrs if isinstance(attr, WidgetSetting)]

def xxx____():
    attr_list = dir(widget_class)
    import logging
    logging.warning(str(attr_list))
    settings = {}
    for attr in attr_list:
        setting = getattr(widget_class, attr)
        if isinstance(setting, WidgetSetting):
            settings[attr] = setting
    logging.info('get widget settings:\n' + str(settings))
    return settings
