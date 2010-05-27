#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Blog app management.
'''

import widget

from exweb import context

import manage

appmenus = [
        ('Widget', [
                manage.AppMenuItem(manage.USER_ROLE_ADMINISTRATOR, 'List', 'list_widget'),
                manage.AppMenuItem(manage.USER_ROLE_ADMINISTRATOR, 'Edit', 'edit_instance')
        ])
]

def manage_nav():
    '''
    Get app's navigation settings so user can customize their navigation bar.
    
    Returns:
        A list contains (title, url).
    '''
    return []

def manage_app(user, action, **args):
    f = ''.join(['__handle_', context.method, '_', action, '()'])
    # we are going to call function by name '__handle_' + (get or post) + _ + action
    return eval(f)

def get_default_settings(w):
    attr_list = dir(w)
    setting_dict = {}
    for attr in attr_list:
        setting = getattr(w, attr)
        if isinstance(setting, widget.WidgetSetting):
            setting_dict[attr] = setting
    return setting_dict

def get_installed_widgets_details():
    dict = widget.get_installed_widgets()
    installed_widgets = []
    for mod_name in dict:
        mod = dict[mod_name]
        w = {
                'id' : mod_name,
                'name' : getattr(mod, 'name', mod_name),
                'author' : getattr(mod, 'author', '(unknown)'),
                'description' : getattr(mod, 'description', '(no description)'),
                'url' : getattr(mod, 'url', ''),
                'class' : mod.Widget,
                'settings' : get_default_settings(mod.Widget)
        }
        installed_widgets.append(w)
    return installed_widgets

def __handle_get_edit_instance():
    # get widget instances of default group:
    instances = widget.get_widget_instances()
    all_settings = widget.get_all_instances_settings()
    widget.bind_instance_model(instances, all_settings)
    for instance in instances:
        wclass = widget.get_installed_widget(instance.widget_id)
        import logging
        logging.warning('\n\n\n$$\n\n' + str(wclass))
        def_setting_dict = widget.get_widget_settings(wclass)
        logging.warning('\n\n\n###\n\n\n' + str(def_setting_dict))
        ins_settings = widget.get_instance_settings(instance)
        # attach ins_settings to def_settings:
        for key in def_setting_dict:
            for ins_setting in ins_settings:
                if key==ins_setting.setting_name:
                    def_setting_dict[key].value = ins_setting.setting_value
        instance.settings = def_setting_dict

    return {
            'template' : 'widget_edit.html',
            'setting_to_html' : setting_to_html,
            'instances' : instances,
            'installed_widgets' : get_installed_widgets_details()
    }

def __handle_post_edit_instance():
    form = context.form
    if form.get('btn')=='add':
        # add a new widget instance:
        widget_id = form.get('widget_id')
        max = len(widget.get_widget_instances())
        instance = widget.WidgetInstance(widget_id=widget_id, widget_order=max)
        instance.put()
    return __handle_get_edit_instance()

def __handle_get_list_widget():
    ' list all widgets '
    return {
            'template' : 'widget_list.html',
            'installed_widgets' : get_installed_widgets_details()
    }

def setting_to_html(name, widget_setting):
    '''
    Generate HTML input for WidgetSetting.
    
    Returns:
      HTML code like '<input name=.../>'
    '''
    if isinstance(widget_setting, widget.WidgetSelectSetting):
        list = [r'<select name="%s">' % name]
        for opts in widget_setting.selections:
            if opts[0]==widget_setting.default:
                list.append(r'<option value="%s" selected="selected">%s</option>' % opts)
            else:
                list.append(r'<option value="%s">%s</option>' % opts)
        list.append('</select>')
        return ''.join(list)
    if isinstance(widget_setting, widget.WidgetCheckedSetting):
        if widget_setting.default==widget_setting.value:
            return '<label><input name="%s" type="checkbox" value="%s" checked="checked"/>%s</label>' % (name, widget_setting.default, widget_setting.label)
        return '<label><input name="%s" type="checkbox" value="%s"/>%s</label>' % (name, widget_setting.default, widget_setting.label)
    if isinstance(widget_setting, widget.WidgetPasswordSetting):
        return '<input name="%s" type="password" value="%s" maxlength="255"/>' % (name, widget_setting.default)
    return '<input name="%s" type="text" value="%s" maxlength="255"/>' % (name, widget_setting.default)
