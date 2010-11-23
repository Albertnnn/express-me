#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Widget definition
'''

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import os

class WidgetSetting(object):
    '''
    settings of a widget class, display as input.
    '''
    __slot__ = ('default', 'required', 'description', 'value', 'pattern')

    def __init__(self, **kw):
        '''
        Init WidgetSetting by kw args that support default='', required=False, 
        description='', value=None, pattern='^.*$'.
        '''
        default = kw.get('default', '')
        required = kw.get('required', False)
        description = kw.get('description', '')
        value = kw.get('value', None)
        pattern = kw.get('pattern', '^.*$')
        if not isinstance(default, basestring):
            raise ValueError('\'default\' must be str or unicode.')
        if not isinstance(required, bool):
            raise ValueError('\'required\' must be bool.')
        if not isinstance(description, basestring):
            raise ValueError('\'description\' must be str or unicode.')
        if not isinstance(pattern, str):
            raise ValueError('\'pattern\' must be str.')
        self.default = default
        self.required = required
        self.description = description
        self.pattern = pattern
        if value:
            self.value = value
        else:
            self.value = default

    def is_modified(self):
        return self.default!=self.value

    def __str__(self):
        return r'''WidgetSetting(default='%s', required=%s, description='%s', value='%s', pattern='%s')''' % (self.default, self.required, self.description, self.value, self.pattern)

    __repr__ = __str__

class WidgetSelectSetting(WidgetSetting):
    '''
    Display as a select input.
    '''
    def __init__(self, **kw):
        '''
        Add selections as kw args that contains list of (key, value, group=None).
        '''
        super(WidgetSelectSetting, self).__init__(**kw)
        self.selections = kw.get('selections', [])

class WidgetCheckedSetting(WidgetSetting):
    '''
    Display as a checked input.
    '''
    def __init__(self, **kw):
        '''
        Add label.
        '''
        default = kw.get('default', 'False')
        super(WidgetCheckedSetting, self).__init__(default=default, required=kw.get('required', False), description=kw.get('description', ''), value=kw.get('value'), pattern='^(True|False)$')
        self.label = kw.get('label', '')

class WidgetPasswordSetting(WidgetSetting):
    '''
    Display as a password input.
    '''
    pass

class WidgetModel(object):

    title = WidgetSetting(description='Widget title (leave empty to hide title)', default='Widget')

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
    logging.info('get widget settings:\n' + str(settings))
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
