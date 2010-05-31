#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Widget definition
'''

from google.appengine.ext import db

import os

DEFAULT_GROUP = 'default'

class WidgetSetting(object):
    '''
    settings of a widget class.
    '''
    __slot__ = ('default', 'required', 'description', 'value')

    def __init__(self, default='', required=False, description='', value=None):
        if not isinstance(default, basestring):
            raise ValueError('\'default\' must be str or unicode.')
        if not isinstance(required, bool):
            raise ValueError('\'required\' must be bool.')
        if not isinstance(description, basestring):
            raise ValueError('\'description\' must be str or unicode.')
        self.default = default
        self.required = required
        self.description = description
        if value is None:
            self.value = default
        else:
            self.value = value

    def is_modified(self):
        return self.default!=self.value

class WidgetSelectSetting(WidgetSetting):
    '''
    Display as a select input.
    '''
    def __init__(self, selections, default='', required=False, description='', value=None):
        '''
        Add selections as a list that contains (key, value).
        '''
        super(WidgetSelectSetting, self).__init__(default, required, description, value)
        self.selections = selections

class WidgetCheckedSetting(WidgetSetting):
    '''
    Display as a checked input.
    '''
    def __init__(self, label, default='False', required=False, description='', value=None):
        '''
        Add label.
        '''
        super(WidgetCheckedSetting, self).__init__(default, required, description, value)
        self.label = label

class WidgetPasswordSetting(WidgetSetting):
    '''
    Display as a password input.
    '''
    pass

class WidgetModel(object):

    title = WidgetSetting(description='Widget title (leave empty to hide title)', default='')

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

    def load(self, id, model):
        self.__id__ = id
        for key, value in model.items():
            self.__setattr__(key, value)

    def render(self):
        buffer = ['<div class="widget" id="']
        buffer.append(self.__id__)
        buffer.append('">')
        if self.title:
            buffer.append('<h3 class="widget-title">')
            buffer.append(self.title)
            buffer.append('</h3>')
        buffer.append('<div class="widget-content">')
        buffer.append(self.get_content())
        buffer.append('</div></div>')
        return ''.join(buffer)

    def get_content(self):
        '''
        Expect to override by subclass.
        '''
        return ''.join([
                '<p>Widget ',
                self.__class__.__name__,
                '@',
                self.__id__,
                '</p>'
        ])

# db models:

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

class WidgetInstanceSetting(db.Model):
    '''
    store settings of widget instance
    '''
    widget_group = db.StringProperty(required=True, default=DEFAULT_GROUP)
    widget_instance = db.ReferenceProperty(reference_class=WidgetInstance, required=True)
    setting_name = db.StringProperty(required=True)
    setting_value = db.StringProperty()

# helper class for db models:

def get_installed_widget(widget_id):
    '''
    Get a installed widget class by id (parent package name)
    
    Args:
      widget_id: widget id, the same as module name.
    
    Returns:
      Widget class.
    '''
    if isinstance(widget_id, unicode):
        widget_id = widget_id.encode('utf-8')
    return __import__('widget.installed.' + widget_id, fromlist=[widget_id]).Widget

def get_installed_widgets():
    '''
    Get all widgets installed in under /widget/installed/.
    
    Args:
        None
    
    Returns:
        Dict that contains widget id (parent package name) as key and Widget class as value.
    '''
    root = os.path.split(os.path.dirname(__file__))[0]
    widget_root = os.path.join(root, 'widget', 'installed')
    widgets = os.listdir(widget_root)
    valid_widgets = [w for w in widgets if __is_valid_widget(widget_root, w)]
    dict = {}
    for w in valid_widgets:
        dict[w] = __import__('widget.installed.' + w, fromlist=[w])
    return dict

def __is_valid_widget(widget_root, widget):
    'detect if this dir contains a valid widget'
    dir = os.path.join(widget_root, widget)
    return os.path.isdir(dir) and os.path.isfile(os.path.join(dir, '__init__.py'))

def get_widget_count(group=DEFAULT_GROUP):
    '''
    Get how many widgets in a group.
    
    Args:
      group: group name, default to DEFAULT_GROUP ('default').
    
    Return:
      int. How many widgets.
    '''
    return WidgetInstance.all().filter('widget_group ==', group).count(100)

def create_widget_instance(id, settings=None, group=DEFAULT_GROUP):
    '''
    Create a new widget instance.
    
    Args:
      widget_id: Widget id (same as parent package name).
      settings: List of WidgetSetting. default to None.
      widget_group: Group name. default to DEFAULT_GROUP.
    
    Return:
      A WidgetInstance object stored in db.
    '''
    instance = WidgetInstance(
            widget_id=id,
            widget_group=group,
            widget_order=get_widget_count(group)
    )
    instance.put()
    if settings:
        for setting in settings:
            ws = WidgetInstanceSetting(
                    widget_group=group,
                    widget_instance=instance,
                    setting_name=setting.name,
                    setting_value=setting.value
            )
            ws.put()
    return instance

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

def get_widget_instance(key):
    '''
    Get widget instance by key.
    '''
    return WidgetInstance.get(key)

def get_widget_instances(widget_group=DEFAULT_GROUP):
    '''
    get widget instances as list contains WidgetInstance objects by group name.
    
    Args:
        widget_group: group name, default to DEFAULT_GROUP.
    Returns:
        list of WidgetInstance objects.
    '''
    return WidgetInstance.all().filter('widget_group ==', widget_group).order('widget_order').fetch(100)

def get_widget_settings(widget_class):
    '''
    Get widget settings.
    
    Args:
      Widget class.
    
    Return:
      Dict contains key as setting name, value as WidgetSetting object.
    '''
    attr_list = dir(widget_class)
    import logging
    logging.warning(str(attr_list))
    settings = {}
    for attr in attr_list:
        setting = getattr(widget_class, attr)
        if isinstance(setting, WidgetSetting):
            settings[attr] = setting
    return settings

def bind_instance_model(instances, settings):
    '''
    Bind models to instances. Each instance object will attach a 'model' field which is 
    a dict.
    '''
    # build setting map, key=instance.key, value=[list of instance_setting]
    d_settings = {}
    import logging
    for setting in settings:
        key = str(setting.widget_instance.key())
        logging.warning('Process setting for instance: ' + key)
        if key in d_settings:
            d_settings[key].append(setting)
        else:
            d_settings[key] = [setting]
    logging.warning('Processed settings map: ' + str(d_settings))
    for instance in instances:
        widget_class = get_installed_widget(instance.widget_id)
        instance.widget_class = widget_class
        key = str(instance.key())
        list = d_settings.pop(key, [])
        logging.warning('Prepare instance settings: ' + str(list))
        instance.model = merge_settings(widget_class, list)

def get_all_instances_settings(group=DEFAULT_GROUP):
    '''
    Get widget instances settings.
    
    Args:
      Group name, default to DEFAULT_GROUP.
    Returns:
      List of WidgetInstanceSetting objects.
    '''
    return WidgetInstanceSetting.all().filter('widget_group', group).fetch(1000)

def get_instance_settings(widget_instance):
    '''
    Get widget instance settings.
    
    Args:
      Widget instance object.
    
    Return:
      List of WidgetInstanceSetting objects.
    '''
    return WidgetInstanceSetting.all().filter('widget_instance', widget_instance).fetch(100)

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

def merge_settings(widget_class, instance_settings):
    '''
    Merge settings of dict of WidgetSetting and list of WidgetInstanceSetting. 
    Instance settings will override widget settings.
    
    Args:
      widget_class: Widget class.
      instance_settings: list of InstanceSetting.
    
    Returns:
      Dict contains key, value of settings.
    '''
    setting_dict = get_widget_settings(widget_class)
    import logging
    logging.warning('Load widget class setting for ' + str(widget_class))
    logging.warning('Settings: ' + str(setting_dict))
    settings = {}
    # set default value of all settings:
    for key in setting_dict:
        settings[key] = setting_dict[key].default
    logging.warning('Init settings: ' + str(settings))
    # override instance settings:
    for instance_setting in instance_settings:
        key = instance_setting.setting_name
        if key in settings:
            settings[key] = instance_setting.setting_value
    logging.warning('Override settings: ' + str(settings))
    return settings


############ TODO #################

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
#    for attr_name in attr_names:
#        attr_value = getattr(w, attr_name)
#        if isinstance(attr_value, SettingModel):
#            d[attr_name] = attr_value.get_value(settings.get(attr_name, None))

# widget API class:
