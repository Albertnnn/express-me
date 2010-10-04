#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Encoding utils for HTML, XML, JavaScript, etc.
'''

def encode_html(str):
    '''
    Encode html.
    
    Args:
        str: string to encode.
    Returns:
        str encoded with utf-8.
    '''
    if isinstance(str, unicode):
        str = str.encode('utf-8')
    return str.replace('&', '&amp;') \
              .replace('<', '&lt;') \
              .replace('>', '&gt;') \
              .replace('"', '&quot;')

def encode_json(str):
    '''
    Encode json.
    
    Args:
        str: string to encode.
    Returns:
        str encoded with utf-8.
    '''
    if isinstance(str, unicode):
        str = str.encode('utf-8')
    return str.replace('\\', r'\\') \
              .replace('"', r'\"') \
              .replace('/', r'\/') \
              .replace('\n', r'\n') \
              .replace('\r', r'\r')
