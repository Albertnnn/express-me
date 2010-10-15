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

def get_template_path(appname, view_name, view_dir='view', ext='.html'):
    '''
    Get template path by app name, view name, view dir and view file extension.
    '''
    web_root = os.path.split(os.path.dirname(__file__))[0]
    return os.path.join(web_root, appname, view_dir, '%s%s' % (view_name, ext,))

def import_compiled_template(mod_name):
    '''
    Try to import a compiled template, or None if no such class.
    
    Args:
        mod_name: module name.
    Return:
        CompiledTemplate class.
    '''
    try:
        return __import__(mod_name, fromlist=['CompiledTemplate']).CompiledTemplate
    except ImportError:
        logging.warn('Import %s.%s failed.' % (mod_name, 'CompiledTemplate'))
        return None

def compile_template(appname, view_name, view_dir='view'):
    '''
    Compile a Cheetah template to class.
    
    Args:
        app: app name
        view_name: view name of template.
        view_dir: view dir name, default to 'view'.
    Returns:
        Compiled class content as string.
    '''
    view_path = get_template_path(appname, view_name, view_dir=view_dir)
    logging.info('Compiling view %s...' % view_path)
    return Template.compile(file=view_path, source=None, returnAClass=False, moduleName='compiled.%s.%s.%s' % (appname, view_dir, view_name), className='CompiledTemplate')

def render(appname, model, view_dir='view'):
    '''
    Render a template using the given model.
    
    Args:
        appname: app name.
        model: model as dict.
    '''
    view_name = model.get('__view__')
    if view_name is None:
        raise RenderError('View is not set.')
    cc = import_compiled_template('compiled.%s.%s.%s' % (appname, view_dir, view_name))
    if cc is not None:
        return cc(searchList=[model], filter='WebSafe')
    view_path = get_template_path(appname, view_name, view_dir=view_dir)
    logging.info('Render view at runtime: %s' % view_path)
    if not os.path.isfile(view_path):
        raise RenderError('Template is not found: %s' % view_path)
    return Template(file=view_path, searchList=[model], filter='WebSafe')
