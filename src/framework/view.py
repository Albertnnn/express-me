#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
View rendering using Cheetah.
'''

import os
import logging

from Cheetah.Template import Template

from framework import ApplicationError

class RenderError(ApplicationError):
    '''
    Error when rendering.
    '''
    pass

def render(appname, model):
    '''
    Render a template using the given model.
    
    Args:
        appname: app name.
        model: model as dict.
    '''
    view_name = model.get('__view__')
    if view_name is None:
        return RenderError('View is not set.')
    web_root = os.path.split(os.path.dirname(__file__))[0]
    view_path = os.path.join(os.path.join(web_root, appname, 'view'), *view_name.split('/'))
    logging.info('Render view: %s' % view_path)
    if not os.path.isfile(view_path):
        return RenderError('Template is not found: %s' % view_path)
    return Template(file=view_path, searchList=[model], filter='WebSafe')
