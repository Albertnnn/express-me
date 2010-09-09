#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

from google.appengine.ext import db

DEFAULT_GROUP = 'default'

class WidgetInstance(db.Model):
    '''
    Store widget instance that can display in widget bar.
    
    A widget instance has 3 properties:
    
    widget_group: indicate the widget bar name this widget belongs to. Default to DEFAULT_GROUP ('default').
    widget_id: the widget id, same as parent package name.
    widget_order: the widget order.
    '''
    widget_group = db.StringProperty(required=True, default=DEFAULT_GROUP)
    widget_id = db.StringProperty(required=True)
    widget_order = db.IntegerProperty(required=True)

    def __str__(self):
        return 'WidgetInstance(id=%s)' % self.widget_id

    __repr__ = __str__

class WidgetInstanceSetting(db.Model):
    '''
    store settings of widget instance.
    
    A WidgetInstanceSetting has 4 properties:
    
    widget_group: indicate the widget bar name this widget belongs to. Default to DEFAULT_GROUP ('default').
    widget_instance: widget instance reference.
    setting_name: widget setting name.
    setting_value: widget setting value.
    '''
    widget_group = db.StringProperty(required=True, default=DEFAULT_GROUP)
    widget_instance = db.ReferenceProperty(reference_class=WidgetInstance, required=True)
    setting_name = db.StringProperty(required=True)
    setting_value = db.StringProperty()

    def __str__(self):
        return 'WidgetInstanceSetting(%s=%s)' % (self.setting_name, self.setting_value)

    __repr__ = __str__

def get_instance_settings(widget_instance):
    '''
    Get widget instance settings.
    
    Args:
      Widget instance object.
    
    Return:
      List of WidgetInstanceSetting objects.
    '''
    return WidgetInstanceSetting.all().filter('widget_instance', widget_instance).fetch(100)

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

def delete_widget_instance(key):
    '''
    Delete a Widget instance and all its settings.
    
    Args:
      key: Widget instance key.
    Returns:
      None
    '''
    instance = WidgetInstance.get(key)
    db.delete(get_instance_settings(instance))
    instance.delete()
