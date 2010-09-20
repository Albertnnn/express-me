#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
app management for User, global settings.
'''

from exweb import context
from manage import shared
import manage
import appconfig

appmenus = [
        ('User', [
                shared.AppMenuItem(shared.USER_ROLE_ADMINISTRATOR, 'Edit', 'edit_user'),
                shared.AppMenuItem(shared.USER_ROLE_ADMINISTRATOR, 'Add New', 'add_user'),
                shared.AppMenuItem(shared.USER_ROLE_SUBSCRIBER, 'Your Profile', 'profile')
        ]),
        ('Setting', [
                shared.AppMenuItem(shared.USER_ROLE_ADMINISTRATOR, 'Navigation', 'navigation'),
                shared.AppMenuItem(shared.USER_ROLE_ADMINISTRATOR, 'Theme', 'theme'),
                shared.AppMenuItem(shared.USER_ROLE_ADMINISTRATOR, 'Settings', 'setting'),
                shared.AppMenuItem(shared.USER_ROLE_ADMINISTRATOR, 'Storage', 'storage')
        ])
]

def manage_app(user, action, **args):
    f = ''.join(['__handle_', context.method, '_', action, '()'])
    # we are going to call function by name '__handle_' + (get or post) + _ + action
    return eval(f)

def __handle_post_navigation():
    form = context.form
    for i in range(manage.NAV_MAX):
        key_t = 'title_%d' % i
        key_u = 'url_%d' % i
        t = form.get_escape(key_t, '')
        u = form.get(key_u, '')
        if t and u:
            shared.save_setting('navigation', key_t, t)
            shared.save_setting('navigation', key_u, u)
    dict = __handle_get_navigation()
    dict['message'] = 'Your navigations are saved.'
    return dict

def __handle_get_navigation():
    guides = [('- Select -', '#'), ('Home', '/')]
    for appname in appconfig.apps:
        module = __import__(appname + '.appmanage')
        manage_nav = getattr(module.appmanage, 'manage_nav', None)
        if callable(manage_nav):
            guides.extend(manage_nav())
    guides.append(('Custom', ''))
    navs = shared.get_settings('navigation')
    if not navs:
        navs['title_0'] = 'Home'
        navs['url_0'] = '/'
    navigations = []
    for i in range(manage.NAV_MAX):
        title = ''
        title_key = 'title_%d' % i
        if title_key in navs:
            title = navs[title_key]
        url = ''
        url_key = 'url_%d' % i
        if url_key in navs:
            url = navs[url_key]
        navigations.append( { 'title' : title, 'url' : url } )
    return {
            'template' : 'navigation.html',
            'guides' : guides,
            'navigations' : navigations
    }

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

def __handle_get_setting():
    settings = shared.get_settings('global')
    return {
            'template' : 'setting.html',
            # site settings:
            'site_title' : __get_setting(settings, 'site_title', 'ExpressMe'),
            'site_subtitle' : __get_setting(settings, 'site_subtitle', 'powered by ExpressMe'),
            # format settings:
            'format_pagesize' : __get_setting(settings, 'format_pagesize', '10'),
            'format_date' : __get_setting(settings, 'format_date', '%Y-%m-%d'),
            'format_time' : __get_setting(settings, 'format_time', '%H:%M:%S'),
            'format_tz' : __get_setting(settings, 'format_tz', 'UTC'),
            # comment settings:
            'comment_show' : __get_setting(settings, 'comment_show', 'True'),
            'comment_allow' : __get_setting(settings, 'comment_allow', 'registered'),
            # feed settings:
            'feed_number' : __get_setting(settings, 'feed_number', '20'),
            'feed_full' : __get_setting(settings, 'feed_full', 'True'),
            'feed_proxy' : __get_setting(settings, 'feed_proxy', ''),
            # add more:
            '__more__' : '__todo__'
    }

def __handle_post_setting():
    '''
    Save all settings
    '''
    form = context.form
    shared.save_setting('global', 'site_title', form.get('site_title'))
    shared.save_setting('global', 'site_subtitle', form.get('site_subtitle'))
    dict = __handle_get_setting()
    dict['message'] = 'Your settings are saved.'
    return dict

def __get_setting(all_settings, key, default_value=''):
    if key in all_settings:
        return all_settings[key]
    return default_value

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

def __handle_get_edit_user():
    return {
            'template' : 'user_edit.html',
            'get_role_name' : shared.get_role_name,
            'users' : shared.get_users()
    }

def __handle_get_add_user():
    return {
            'template' : 'user_add.html'
    }

def __handle_post_add_user():
    form = context.form
    role = int(form.get('role'))
    email = form.get('email')
    hashed_passwd = form.get('passwd')
    nicename = form.get('nicename')
    website = form.get('website')
    user = shared.create_user(role, email, hashed_passwd, nicename, website)
    return {
            'template' : 'message.html',
            'message' : 'New user created',
            'detail' : 'User has been created successfully',
            'url' : '?app=manage&action=user_add',
            'url_title' : 'Add Another User'
    }

def __handle_get_profile():
    return {
            'template' : 'user_profile.html',
            'user' : context.user
    }

def __handle_post_profile():
    form = context.form
    nicename = form.get('nicename')
    website = form.get('website')
    hashed_passwd = form.get('passwd', '')
    user = shared.get_user_by_email(context.user.user_email)
    user.user_nicename = nicename
    user.user_website = website
    if hashed_passwd:
        user.user_passwd = hashed_passwd
    user.put()
    return {
            'template' : 'user_profile.html',
            'message' : (hashed_passwd!='') and 'Your profile and password have been updated.' or 'Your profile has been updated.',
            'user' : user
    }
