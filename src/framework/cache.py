#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Simple functions to make ease of use memcache.
'''

from google.appengine.api import memcache as memcache

def set(key, value, time=0):
    '''
    Put the value into cache for a given key.
    
    Args:
        key: key as str.
        value: value as object.
        time: expires time, default to 0 (forever).
    '''
    memcache.set(key, value, time)

def get(key, func_or_value=None, time=0):
    '''
    Retrieve the value from cache for a given key. 
    If value is not found in cache, and func_or_value is None, 
    then the None will return.
    If func_or_value is a function, cache will be updated with the 
    value returned by function.
    If func_or_value is not a function, then it must be a value, and 
    cache will be updated with the value.
    
    Args:
        key: the key of the value.
        func_or_value: a function or value.
        time: expires time, default to 0 (forever).
    Returns:
        value stored in cache, or None if not found.
    '''
    value = memcache.get(key)
    if value is None:
        if callable(func_or_value):
            value = func_or_value()
        else:
            value = func_or_value
        memcache.set(key, value, time)
    return value

def incr(key):
    memcache.incr(key)
