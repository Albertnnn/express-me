#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Containing classes of exweb mvc framework:
context: thread local object which has properties:
  appid: application id
  method: 'get' or 'post'
  request: http request object
  response: http response object
  query: query object that contains key-value(s) pair from http request
  form: alias of query
  set_cookie: function to set cookie
  remove_cookie: function to remove cookie

HttpError: base error
HttpForbiddenError: 403 Forbidden
HttpMethodNotAllowedError: 405 Method Not Allowed
HttpNotFoundError: 404 Not Found
HttpRedirectError: 302 Redirect

decorators for url mapping:
@get: url mapping for http get.
@post: url mapping for http post.
@mapping: url mapping for both get and post.
@raw_mapping: raw url mapping using regular expression for both get and post.
'''

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import cgi
from threading import local

context = local()

class HttpError(StandardError): pass

class HttpSignOnError(HttpError):
    def __init__(self, signon_addr):
        self.signon = signon_addr

class HttpForbiddenError(HttpError): pass

class HttpMethodNotAllowedError(HttpError): pass

class HttpNotFoundError(HttpError): pass

class HttpBadRequestError(HttpError): pass

class HttpRedirectError(HttpError):
    def __init__(self, uri):
        HttpError.__init__(self)
        self.uri = uri

class Headers(object):
    '''
    Headers is a wrapper for http headers and looks like a dict.
    '''
    def __init__(self, request):
        self.request = request

    def get(self, header_name, default_value=None):
        if header_name in self.request.headers:
            return self.request.headers[header_name]
        return default_value

class Form(object):
    '''
    Form is either a Form by http post, or query parameters by http get.
    '''
    def __init__(self, request):
        self.request = request

    def get_escape(self, argument_name, default_value='', allow_multiple=False):
        '''
        The same as get(), but return html-encoded string.
        '''
        return cgi.escape(self.request.get(argument_name, default_value, allow_multiple))

    def get(self, argument_name, default_value='', allow_multiple=False):
        '''
        Returns the query or POST argument with the given name.
        
        We parse the query string and POST payload lazily, so this will be a
        slower operation on the first call.
        
        Args:
            argument_name: the name of the query or POST argument
            default_value: the value to return if the given argument is not present
            allow_multiple: return a list of values with the given name (deprecated)

        Returns:
            If allow_multiple is False (which it is by default), we return the first
            value with the given name given in the request. If it is True, we always
            return an list.
        '''
        return self.request.get(argument_name, default_value, allow_multiple)

    def get_all_escape(self, argument_name):
        '''
        The same as get_all(), but return html-encoded string list.
        '''
        all = self.get_all(argument_name)
        return [cgi.escape(a) for a in all]

    def get_all(self, argument_name):
        '''
        Returns a list of query or POST arguments with the given name.
        
        We parse the query string and POST payload lazily, so this will be a
        slower operation on the first call.
        
        Args:
            argument_name: the name of the query or POST argument
        
        Returns:
            A (possibly empty) list of values.
        '''
        return self.request.get_all(argument_name)

    def get_file(self, argument_name):
        '''
        Get uploaded filename and content.
        
        Args:
            argument_name: Field name of uploaded file
        
        Returns:
            None if no such uploaded file, or a Tuple of (file_name as str, file_content as str).
        '''
        form = cgi.FieldStorage()
        if not form.has_key(argument_name):
            return None
        item = form[argument_name]
        if item.file is None:
            return None
        return item.filename, item.file.read()

    def arguments(self):
        '''
        Returns a list of the arguments provided in the query and/or POST.
        
        The return value is a list of strings.
        '''
        return self.request.arguments()

def raw_mapping(url):
    '''
    decorator of @raw_mapping() that support get and post.
    WARNING: for regular express expert only!
    
    The regular expression MUST NOT start with '^' and end with '$'.
    
    Args:
        url: regular expression string.
    
    Returns:
        decorated function.
    '''
    def execute(f):
        def wrapper(*args, **kw):
            return f(*args, **kw)
        wrapper.url = url
        wrapper.support_get = True
        wrapper.support_post = True
        wrapper.raw_mapping = True
        wrapper.__name__ = f.__name__
        return wrapper
    return execute

def mapping(url=None):
    '''
    decorator of @mapping() that support get and post
    
    Args:
        url: string like '/$/$.html', default value: None
    
    Returns:
        decorated function.
    '''
    def execute(f):
        def wrapper(*args, **kw):
            return f(*args, **kw)
        if url==None:
            wrapper.url = '/' + f.__name__
        else:
            wrapper.url = url
        wrapper.support_get = True
        wrapper.support_post = True
        wrapper.raw_mapping = False
        wrapper.__name__ = f.__name__
        return wrapper
    return execute

def get(url=None):
    '''
    decorator of @get() that support get only
    
    Args:
        url: string like '/$/$.html', default value: None
    
    Returns:
        decorated function.
    '''
    def execute(f):
        def wrapper(*args, **kw):
            return f(*args, **kw)
        if url==None:
            wrapper.url = '/' + f.__name__
        else:
            wrapper.url = url
        wrapper.support_get = True
        wrapper.support_post = False
        wrapper.raw_mapping = False
        wrapper.__name__ = f.__name__
        return wrapper
    return execute

def post(url=None):
    '''
    decorator of @post() that support post only
    
    Args:
        url: string like '/$/$.html', default value: None
    
    Returns:
        decorated function.
    '''
    def execute(f):
        def wrapper(*args, **kw):
            return f(*args, **kw)
        if url==None:
            wrapper.url = '/' + f.__name__
        else:
            wrapper.url = url
        wrapper.support_get = False
        wrapper.support_post = True
        wrapper.raw_mapping = False
        wrapper.__name__ = f.__name__
        return wrapper
    return execute

class Filter(object):
    def process(self, chain):
        chain.next()
