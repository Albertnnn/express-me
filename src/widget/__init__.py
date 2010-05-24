#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Widget definition
'''

from google.appengine.ext import db

import os

def get_installed_widgets():
    '''
    Get all widgets installed in ExpressMe.
    
    Args:
        None
    
    Returns:
        Dict that contains widget name (short name) as key and Widget module as value.
    '''
    root = os.path.split(os.path.dirname(__file__))[0]
    widget_root = os.path.join(root, 'widget', 'installed')
    widgets = os.listdir(widget_root)
    valid_widgets = [w for w in widgets if __is_valid_widget(widget_root, w)]
    dict = {}
    for w in valid_widgets:
        dict[w] = __import__('widget.installed.' + w, fromlist=[w])
    import logging
    logging.error('#\n#\n#\n#\n#\n#\n'+str(dict))
    return dict

def __is_valid_widget(widget_root, widget):
    dir = os.path.join(widget_root, widget)
    return os.path.isdir(dir) and os.path.isfile(os.path.join(dir, '__init__.py'))

class WidgetSetting():
    ' settings of a widget class '
    __slot__ = ('default', 'required', 'description')

    def __init__(self, default='', required=False, description=''):
        if not isinstance(default, basestring):
            raise ValueError('\'default\' must be str or unicode.')
        if not isinstance(required, bool):
            raise ValueError('\'required\' must be bool.')
        if not isinstance(description, basestring):
            raise ValueError('\'description\' must be str or unicode.')
        self.default = default
        self.required = required
        self.description = description

# db models:

class WidgetInstance(db.Model):
    ' store widget instance that can display on pages '
    widget_group = db.StringProperty(required=True, default='default')
    widget_name = db.StringProperty(required=True)
    widget_order = db.IntegerProperty(required=True)

class WidgetInstanceSetting(db.Model):
    ' store settings of widget instance '
    widget_instance = db.ReferenceProperty(reference_class=WidgetInstance, required=True)
    setting_key = db.StringProperty(required=True)
    setting_value = db.StringProperty()

# helper class for db models:

def create_widget_instance(name, group='default'):
    max = WidgetInstance.all().filter('widget_group ==', group).count(100)
    instance = WidgetInstance(widget_name=name, widget_group=group, widget_order=max)
    instance.put()
    return instance

def get_widget_instances(widget_group='default'):
    '''
    get widget instances as list contains WidgetInstance objects by group name.
    
    Args:
        widget_group: group name, default to 'default'.
    Returns:
        list of WidgetInstance objects.
    '''
    return WidgetInstance.all().filter('widget_group ==', widget_group).order('widget_order').fetch(100)

def get_widget_settings(widget_instance):
    '''
    get widget settings as dict which contains key-value pairs (both str/unicode).
    
    Args:
        widget_instance: WidgetInstance object.
    Returns:
        Settings as dict which both key and value are str/unicode.
    '''
    list = WidgetSetting.all().filer('widget_instance ==', widget_instance).fetch(100)
    d = {}
    for setting in list:
        d[setting.setting_key] = setting.setting_value
    return d

def instantiate_widget(widget_instance):
    '''
    Instantiate a Widget object by given instance.
    
    Args:
        widget_instance: WidgetInstance object.
    Returns:
        Widget object.
    '''
    settings = get_widget_settings()
    m = __import__('widget.installed.' + widget_instance.widget_name, fromlist=[widget_instance.widget_name])
    w = m.Widget()
    attr_names = [a for a in dir(w) if not a.startswith('__')]
    d = {}
    for attr_name in attr_names:
        attr_value = getattr(w, attr_name)
        if isinstance(attr_value, SettingModel):
            d[attr_name] = attr_value.get_value(settings.get(attr_name, None))

# widget API class:

class SettingModel(type):
    ' Meta-class for initializing Setting '
    pass

class WidgetSettings(object):

    __slots__ = ('name', 'required', 'description', 'maxlength', 'default')

    def __init__(self, required=False, description='', maxlength=200, default=None):
        self.required = required
        self.description = description
        self.maxlength = maxlength
        self.default = default

    def validate(self, value):
        return True

    def get_value(self, value=None):
        if value:
            if self.validate(value):
                return value
        return self.default

class WidgetSelectSetting(WidgetSetting):
    pass

class WidgetPasswordSetting(WidgetSetting):

    def __init__(self, required=False, description='', maxlength=200, default=None):
        super(WidgetPasswordSetting, self).__init__(required, description, maxlength, default)

class WidgetModel(object):

    def handle_request(self, request, response, parameters):
        '''
        Handle a AJAX request that makes a Widget can interact with users.
        
        NOTE that the HTTP request is initiate from widget's HTML snippets by JavaScript, 
        and unlike the normal app-dispatcher-handler, HTTP response must be handled and 
        any returning value will be ignored.
        '''
        out = response.out
        out.write('<html><head><title>Widget Debug</title></head><body><p>Request: %s</p><p>Method: %s</p><p>Parameters:</p>' % (request.url, request.method.lower()))
        if parameters and len(parameters)>0:
            for key, value in parameters.iteritems():
                out.write('<p>&nbsp;&nbsp;%s = %s</p>' % (key, value))
        else:
            out.write('<p>&nbsp;&nbsp;<i>None</i></p>')
        out.write('</body></html>')

    def load(self):
        return {
                'title' : 'Widget Title',
                'content' : 'Widget Content in <strong>HTML</strong> format'
        }

    def render(self, data):
        title = ''
        if 'title' in data:
            title = data['title']
        content = ''
        if 'content' in data:
            content = data['content']
        buffer = ['<div class="widget" id="']
        buffer.append(self.__class__.__module__.replace('.', '_'))
        buffer.append('">')
        if title:
            buffer.append('<h3 class="widget-title">')
            buffer.append(title)
            buffer.append('</h3>')
        buffer.append('<div class="widget-content">')
        buffer.append(content)
        buffer.append('</div></div>')
        return ''.join(buffer)
