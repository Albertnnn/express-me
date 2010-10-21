#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

Deprecated = True

'''
app management for User, global settings.
'''

from manage import shared
import manage
import appconfig

def __handle_get_theme():
    '''
    Display all themes under dir '/theme'
    '''
    themes = manage.get_themes()
    selected = shared.get_setting('theme', 'selected', '')
    if not selected in themes:
        selected = themes[0]
    return {
            'template' : 'theme.html',
            'themes' : themes,
            'selected' : selected
    }

def __handle_post_theme():
    selected = context.form.get('theme', '')
    dict = __handle_get_theme()
    if selected in dict['themes']:
        shared.save_setting('theme', 'selected', selected)
        dict['selected'] = selected
        dict['message'] = 'New theme applied. <a href="/" target="_blank">View Site</a>'
    return dict

def __handle_get_storage():
    import storage
    photo_module_names = storage.find_photo_modules()
    photo_providers = [mod.PhotoProvider for mod in [__import__('storage.photo.' + p, globals(), locals(), ['PhotoProvider']) for p in photo_module_names]]
    settings = shared.get_settings('storage')
    def __get_provider_setting(provider, name):
        key = provider.__module__.replace('.', '_') + '_' + name
        if key in settings:
            return settings[key]
        return ''
    return {
            'template' : 'storage.html',
            'get_provider_setting' : __get_provider_setting,
            # photo storage:
            'photo_providers' : photo_providers,
            'photo_provider' : __get_setting(settings, 'photo_provider', ''),
            # file storage:
            'file_provider' : __get_setting(settings, 'file_provider', ''),
            # use proxy:
            'photo_proxied' : __get_setting(settings, 'photo_proxied', ''),
            'file_proxied' : __get_setting(settings, 'file_proxied', '')
    }

def __handle_post_storage():
    form = context.form
    args = form.arguments()
    if 'photo_provider' in args:
        shared.save_setting('storage', 'photo_provider', form.get('photo_provider'))
        photo_args = [arg for arg in args if arg.startswith('storage_photo_')]
        for arg in photo_args:
            shared.save_setting('storage', arg, form.get(arg, ''))
    shared.save_setting('storage', 'photo_proxied', form.get('photo_proxied'))
    shared.save_setting('storage', 'file_proxied', form.get('file_proxied'))
    dict = __handle_get_storage()
    dict['message'] = 'Your storage settings are saved.'
    return dict
