#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Widget app management.
'''

from framework import store

from manage import AppMenu
from manage import AppMenuItem

from widget import model
import theme

def get_menus():
    '''
    Get menus for management.
    '''
    widget = AppMenu('Widget',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'All Widgets', 'list_widget'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Sidebars', 'edit_sidebar')
    )
    return (widget,)

def get_navigation():
    '''
    Get navigation menu.
    '''
    return []

def get_default_settings(w):
    attr_list = dir(w)
    setting_dict = {}
    for attr in attr_list:
        setting = getattr(w, attr)
        if isinstance(setting, widget.WidgetSetting):
            setting_dict[attr] = copy.deepcopy(setting)
    return setting_dict

def get_installed_widgets_details():
    dict = widget.get_installed_widgets()
    installed_widgets = []
    for mod_name in dict:
        mod = dict[mod_name]
        w = {
                'id' : mod_name,
                'name' : getattr(mod.Widget, 'widget_name', mod_name),
                'author' : getattr(mod.Widget, 'widget_author', '(unknown)'),
                'description' : getattr(mod.Widget, 'widget_description', '(no description)'),
                'url' : getattr(mod.Widget, 'widget_url', ''),
                'class' : mod.Widget,
                'settings' : get_default_settings(mod.Widget)
        }
        installed_widgets.append(w)
    return installed_widgets

def __handle_get_edit_instance():
    # get widget instances of default group:
    instances = widget.get_widget_instances()
    all_settings = widget.get_all_instances_settings()
    import logging
    for s in all_settings:
        logging.warning('Load all settings: ' + s.setting_name + '=' + s.setting_value)
    widget.bind_instance_model(instances, all_settings)
    for instance in instances:
        wclass = widget.get_installed_widget(instance.widget_id)
        logging.warning('\n\n\n$$\n\n' + str(wclass))
        def_setting_dict = widget.get_widget_settings(wclass)
        logging.warning('\n\n\n###\n\n\n' + str(def_setting_dict))
        ins_settings = store.get_instance_settings(instance)
        # attach ins_settings to def_settings:
        for key in def_setting_dict:
            for ins_setting in ins_settings:
                if key==ins_setting.setting_name:
                    def_setting_dict[key].value = ins_setting.setting_value
        instance.settings = def_setting_dict

    return {
            'template' : 'widget_edit.html',
            'setting_to_html' : widget_setting_to_html,
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
    elif form.get('btn')=='edit':
        # update:
        instance = widget.get_widget_instance(form.get('id'))
        defaults = widget.get_widget_settings(widget.get_installed_widget(instance.widget_id))
        args = form.arguments()
        d = {}
        for arg in args:
            if arg in defaults:
                d[arg] = form.get(arg)
        import logging
        logging.warning('update... ' + str(d))
        store.update_instance_settings(instance, d)
    elif form.get('btn')=='remove':
        # remove:
        store.delete_widget_instance(form.get('id'))
    return __handle_get_edit_instance()

def __handle_get_list_widget():
    ' list all widgets '
    return {
            'template' : 'widget_list.html',
            'installed_widgets' : get_installed_widgets_details()
    }

def widget_setting_to_html(name, widget_setting):
    '''
    Generate HTML input for WidgetSetting.
    
    Returns:
      HTML code like '<input name=.../>'
    '''
    if isinstance(widget_setting, widget.WidgetSelectSetting):
        list = [r'<select name="%s" class="widget-select">' % name]
        for opts in widget_setting.selections:
            if opts[0]==widget_setting.value:
                list.append(r'<option value="%s" selected="selected">%s</option>' % opts)
            else:
                list.append(r'<option value="%s">%s</option>' % opts)
        list.append('</select>')
        return ''.join(list)
    if isinstance(widget_setting, widget.WidgetCheckedSetting):
        if widget_setting.value=='True':
            return '<label><input name="%s" type="checkbox" value="True" checked="checked"/>%s</label>' % (name, widget_setting.label)
        return '<label><input name="%s" type="checkbox" value="True"/>%s</label>' % (name, widget_setting.label)
    if isinstance(widget_setting, widget.WidgetPasswordSetting):
        return '<input name="%s" type="password" value="%s" maxlength="255" class="widget-input"/>' % (name, widget_setting.value)
    return '<input name="%s" type="text" value="%s" maxlength="255" class="widget-input"/>' % (name, widget_setting.value)







#-----------------------------------------------------

def __get_widget_class_info(pkg_name, cls):
    title = getattr(cls, '__title__', pkg_name)
    description = getattr(cls, '__description__', '(no description)')
    author = getattr(cls, '__author__', '(unknown)')
    url = getattr(cls, '__url__', None)
    return {
            'id' : pkg_name,
            'title' : title,
            'description' : description,
            'author' : author,
            'url' : url,
    }

def __get_widget_class_infos():
    widgets = model.get_installed_widgets()
    widgets_infos = [__get_widget_class_info(pkg_name, cls) for pkg_name, cls in widgets.iteritems()]
    widgets_infos.sort(cmp=lambda d1, d2: d1['title'].lower()<d2['title'].lower() and -1 or 1)
    return widgets_infos

def _list_widget(user, app, context):
    return {
            '__view__' : 'manage_widget_list',
            'widgets' : __get_widget_class_infos(),
    }

def _edit_sidebar(user, app, context):
    widgets = __get_widget_class_infos()
    sidebars = [
            model.get_widget_instances(0, False),
    ]
    info = ''
    btn = context.get_argument('btn', '')
    if btn=='add':
        # add a new widget instance:
        widget_name = context.get_argument('widget_name')
        sidebar = int(context.get_argument('sidebar'))
        title = None
        for w in widgets:
            if w['id']==widget_name:
                title = w['title']
                break
        info = 'A new widget "%s" was added to sidebar %s.' % (title,(sidebar+1),)
        model.create_widget_instance(widget_name, sidebar)
    return {
            'info' : info,
            '__view__' : 'manage_sidebar',
            'widgets' : widgets,
            'sidebars' : sidebars,
            'theme' : theme.get_theme_info(theme.get_current_theme()),
    }

def manage(user, app, command, context):
    map = {
           'list_widget' : _list_widget,
           'edit_sidebar' : _edit_sidebar,
    }
    return map[command](user, app, context)
