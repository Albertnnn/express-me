#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
All storage-related class and functions.
'''

from google.appengine.ext import db as db

class StoreError(StandardError):
    pass

class BaseModel(db.Model):
    '''
    Base model for storage which has basic properties.
    '''
    creation_date = db.DateTimeProperty(required=True, auto_now_add=True)
    modified_date = db.DateTimeProperty(required=True, auto_now=True)

    def __getattr__(self, name):
        if name=='id':
            try:
                return str(self.key())
            except db.NotSavedError:
                return None
        if name.endswith('__raw__'):
            return getattr(self, name[:-7])
        raise AttributeError('\'%s\' object has no attribute \'%s\'' % (self.__class__.__name__, name))

MAX_METADATA = 100

def query_metadata(ref, name=None):
    '''
    Query meta data of specific reference (key of Model).
    
    Args:
        ref: key of owner object.
        name: mata data name, default to None.
    Returns:
        dict contains meta data name-value pairs. If name is not None, all names will return.
    '''
    query = MetaData.all().filter('ref =', ref)
    if name is not None:
        query.filter('name =', name)
    map = {}
    for meta in query.fetch(MAX_METADATA):
        map[str(meta.name)] = meta.value
    return map

def save_metadata(ref, **kw):
    '''
    Save new meta data for specific reference.
    '''
    for name, value in kw:
        MetaData(ref=ref, name=name, value=value).put()

def delete_metadata(ref, names):
    '''
    Delete meta data by names.
    '''
    for meta in MetaData.all().filter('ref =', ref).fetch(MAX_METADATA):
        if str(meta.name) in names:
            meta.delete()

class MetaData(db.Model):
    '''
    Store meta data such as web site, twitter, settings, etc.
    '''
    ref = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    value = db.StringProperty(required=True)
