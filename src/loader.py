#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Load template by theme
'''

import os
import manage

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from exweb import context
from exweb.dispatcher import Dispatcher

import widget

def load_template(selected=''):
    '''
    Load template and return its path.
    '''
    themes = manage.get_themes()
    if selected=='':
        selected = manage.get_setting('theme', 'selected', '')
    if not selected in themes:
        selected = themes[0]
    return ('theme', selected, 'template.html')

def update_model(rootpath, appname, model):
    model['site'] = {
            'title' : manage.get_setting('global', 'site_title', 'ExpressMe'),
            'subtitle' : manage.get_setting('global', 'site_subtitle', 'powered by ExpressMe')
    }
    model['navigations'] = manage.get_navigations()
    model['user'] = context.user
    model['app'] = appname
    # set current theme = 'simple':
    theme = manage.get_setting('theme', 'selected', '')
    if not theme:
        themes = manage.get_themes()
        theme = themes[0]
        manage.save_setting('theme', 'selected', theme)
    model['theme'] = theme
    # add widgets:
    #wd = widget.get_installed_widgets()
    #w_list = [x for x in widget.get_widget_instances('default') if x.widget_name in wd]
    
    #if widget_list:
    #    widget.
    #import widget.google_adsense
    #import widget.music_box
    #import widget.subscribe
    #import widget.html
    #ws = [
    #      widget.subscribe.Widget(),
    #      widget.html.Widget(),
    #      widget.music_box.Widget(),
    #      widget.recent_tweets.Widget(),
    #      widget.google_adsense.Widget(),
    #]
    #for w in ws:
    #    w.widget_model = w.load()
    model['widgets'] = []
    # set app_main to path:
    app_main = os.path.join(rootpath, 'theme', theme, appname + '.main.html')
    if not os.path.exists(app_main):
        app_main = os.path.join(rootpath, appname, 'main.html')
    model['app_main'] = app_main
    model['format_datetime'] = lambda d : d.strftime('%Y-%m-%d %H:%M:%S')
    model['format_date'] = lambda d : d.strftime('%Y-%m-%d')
    model['format_time'] = lambda d : d.strftime('%H:%M:%S')

application = webapp.WSGIApplication([('^/.*$', Dispatcher)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
