#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: Michael Liao (askxuefeng@gmail.com)
'''

import os
import re
import time
import urllib

from google.appengine.ext import webapp

from Cheetah.Template import Template

from exweb import context
from exweb import Form
from exweb import Headers
from exweb import HttpNotFoundError
from exweb import HttpRedirectError
from exweb import HttpBadRequestError

import appconfig
import loader

HTTP_400 = '<html><head><title>400 Bad Request</title></head><body><h1>400 Bad Request</h1></body></html>'
HTTP_403 = '<html><head><title>403 Forbidden</title></head><body><h1>403 Forbidden</h1></body></html>'
HTTP_404 = '<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>'

def get_cookie(name):
    '''
    Get cookie by name.
    
    Args:
        name: cookie name as string.
    
    Returns:
        Cookie value, or None if not exist.
    '''
    if not 'Cookie' in context.request.headers:
        return None
    all = context.request.headers['Cookie']
    if all is None:
        return None
    cookies = all.split(';')
    key = name + '='
    for cookie in cookies:
        c = cookie.strip()
        if c.startswith(key):
            return c[len(key):]
    return None

def set_cookie(name, value, max_age=-1, path='/', domain=None, secure=False):
    '''
    Set a cookie to client.
    
    Args:
        name: cookie name.
        value: cookie value.
        max_age: cookie age in seconds, if 0, cookie will be deleted immediately, if <0, ignored. Default to -1.
        path: cookie path, default to '/'.
        domain: domain name, default to None and ignored.
        secure: if cookie is secure, default to False.
    
    Returns:
        None, but cookie was added to response headers.
    '''
    cookie = name + '=' + value + '; path=' + path
    if max_age>=0:
        cookie += time.strftime('; expires=%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(time.time() + max_age))
    if domain is not None:
        cookie = cookie + '; domain=' + domain
    if secure:
        cookie += '; secure'
    context.response.headers.add_header('Set-Cookie', cookie)

def remove_cookie(name, path='/', domain=None, secure=False):
    '''
    Remove cookie by name.
    
    Args:
        name: cookie name.
        path: cookie path, default to '/'.
        domain: domain name, default to None and ignored.
        secure: if cookie is secure, default to False.
    
    Returns:
        None, but cookie was added to response headers and should be removed in client.
    '''
    set_cookie(name, 'deleted', 0, path, domain, secure)

class Dispatcher(webapp.RequestHandler):

    def get(self):
        self.handle('get')

    def post(self):
        self.handle('post')

    def handle_exception(self, exception, debug_mode):
        if isinstance(exception, HttpNotFoundError):
            self.error(404)
            self.response.clear()
            self.response.out.write(HTTP_404)
            return
        if isinstance(exception, HttpRedirectError):
            self.response.set_status(302)
            self.response.headers['Location'] = exception.uri
            self.response.clear()
            return
        if isinstance(exception, HttpBadRequestError):
            self.response.set_status(400)
            self.response.clear()
            self.response.out.write(HTTP_400)
            return
        super(Dispatcher, self).handle_exception(exception, debug_mode)

    def handle(self, method):
        '''
        handle http request
        method: http request method as string, only be 'get' or 'post'
        '''
        # bind request and response to thread local:
        context.appid = os.environ['APPLICATION_ID']
        context.method = method
        context.request = self.request
        context.response = self.response
        context.headers = Headers(self.request)
        context.form = context.query = Form(self.request)
        context.get_cookie = get_cookie
        context.set_cookie = set_cookie
        context.remove_cookie = remove_cookie
        try:
            apps = list(appconfig.apps)
            apps.extend(['widget', 'manage', 'util'])
            path = context.request.path
            if path=='/':
                return self.__render_string('redirect:/' + apps[0])
            n = path.find('/', 1)
            if n==(-1):
                n = len(path)
            appname = path[1:n]
            if not appname in apps:
                raise HttpNotFoundError()
            apppath = path[len(appname)+1:]
            if not apppath.startswith('/'):
                apppath = '/' + apppath
            self.__handle_internal(appname, apppath)
        finally:
            del context.appid
            del context.method
            del context.request
            del context.response
            del context.headers
            del context.query
            del context.form
            del context.set_cookie
            del context.remove_cookie

    def __handle_internal(self, appname, apppath):
        module = __import__(appname + '.app')
        mappings = self.__get_mappings(module.app, context.method)
        for url, fun in mappings.items():
            r = self.__matches(url, apppath, fun.raw_mapping)
            if r is not None:
                args = [urllib.unquote(arg) for arg in r] # decode url parameter
                result = self.__handle_with_filters(fun, args)
                return self.__handle_result(appname, result, fun);
        raise HttpNotFoundError()

    def __handle_with_filters(self, fun, args):
        # BEGIN hardcode:
        from manage.filter import auto_sign_on_filter
        auto_sign_on_filter()
        # END hardcode
        return fun(*args)

    def __handle_result(self, appname, model, f=None):
        if model==None:
            return
        elif isinstance(model, basestring):
            self.__render_string(model)
        elif type(model)==type({}):
            root = os.path.split(os.path.dirname(__file__))[0]
            loader.update_model(root, appname, model)
            template_path = loader.load_template()
            path = os.path.join(root, *template_path)
            self.__render_template(path, model)
        elif type(model)==type(()):
            if len(model)!=2:
                raise ValueError('Tuple must have exact 2 elements')
            if isinstance(model[0], basestring) and type(model[1])==type({}):
                root = os.path.split(os.path.dirname(__file__))[0]
                path = os.path.join(root, appname, model[0])
                self.__render_template(path, model[1])
            else:
                raise ValueError('Tuple must be (\'basestring\', {dict})')

    def __render_template(self, templatepath, model):
        t = Template(file=templatepath, searchList=[model])
        self.response.out.write(t)

    def __render_string(self, s):
        if s.startswith('redirect:'):
            raise HttpRedirectError(s[9:])
        elif s.startswith('json:'):
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(s[5:])
        else:
            self.response.out.write(s)

    def __matches(self, url, apppath, raw_mapping):
        '''
        return match results of url with given apppath.
        return (arg1, arg2, ...) if url is match and extract the args as tuple;
        return None if not match.
        '''
        if raw_mapping:
            p = re.compile('^' + url + '$')
        else:
            p = re.compile('^' + re.escape(url).replace(r'\$', '([^/]*)') + '$')
        m = p.match(apppath)
        if m is not None:
            return m.groups()
        return None

    def __get_mappings(self, module, method):
        fnames = [f for f in dir(module) if callable(getattr(module, f))]
        mapping = {}
        support = 'support_' + method # 'support_get' or 'support_post'
        for f in fnames:
            fun = getattr(module, f)
            if getattr(fun, support, False):
                mapping[getattr(fun, 'url')] = fun
        return mapping
