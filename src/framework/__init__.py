#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

class ApplicationError(StandardError):
    '''
    Base error for ExpressMe application.
    '''
    pass

class ValidationError(ApplicationError):
    '''
    Validation failed.
    '''
    pass

class PermissionError(ApplicationError):
    '''
    Permission denied.
    '''
    pass
