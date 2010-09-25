#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
ExpressMe version definition.
'''

major_version = 1
minor_version = 0

def get_version():
    '''
    Get current version as string
    '''
    return '%d.%d' % (major_version, minor_version)
