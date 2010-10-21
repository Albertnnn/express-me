#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Storage providers.
'''

import os
import re

def find_photo_modules():
    from storage import photo as pkg
    return __find_modules(pkg)

def find_file_modules():
    from storage import file as pkg
    return __find_modules(pkg)

def __find_modules(pkg):
    return [re.sub('\.py$', '', f) for f in os.listdir(os.path.dirname(pkg.__file__)) if f.endswith(".py") and f!="__init__.py"]

class Provider(object):
    pass

class ValidateError(StandardError):
    def __init__(self, message):
        self.message = message

class ProviderSetting(object):
    __slots__ = ('key', 'default', 'required', 'description', 'is_password')
    def __init__(self, key, default, required, description, is_password=False):
        self.key = key
        self.required = required
        self.description = description
        self.is_password = is_password

    def validate(self, value):
        pass
