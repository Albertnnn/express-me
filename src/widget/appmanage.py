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
                manage.AppMenuItem(manage.USER_ROLE_ADMINISTRATOR, 'Edit', 'edit_widget')
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

def __handle_get_edit_widget():
    ' list all widgets '
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
                'enabled' : True
        }
        installed_widgets.append(w)
    return {
            'template' : 'widget_edit_list.html',
            'installed_widgets' : installed_widgets
    }

def __handle_post_add_widget():
    ' add a new widget instance '
    form = context.form
    name = form.get_escape('name')
    group = form.get_escape('group')
    widget.create_widget_instance(name, group)
    return __handle_get_list_widget()

def __handle_post_edit_widget():
    form = context.form
    name = form.get_escape('name')
    description = form.get_escape('description')
    return {
            'template' : 'message.html',
            'message' : 'Category created.',
            'detail' : 'Your category has been created successfully!',
            'url' : '?app=blog&action=post_categories',
            'url_title' : 'Continue'
    }

def __handle_get_tags():
    return {
            'template' : 'post_tags.html'
    }
