#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
All storage-related class and functions.
'''

from google.appengine.ext import db as db

class BaseModel(db.Model):
    '''
    Base model for storage which has basic properties.
    '''

    version = db.IntegerProperty(default=0, required=True)
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
