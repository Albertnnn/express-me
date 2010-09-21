#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Simple anti-bot API for Google reCaptcha service.
'''

TEST_DOMAIN = 'localhost'
TEST_PUB_KEY = '6LeAOr0SAAAAALQX_KWv_JhJpXrHNE5Xo0Z-UJwe'
TEST_PRI_KEY = '6LeAOr0SAAAAAAftuAAf6hI7McUzejjY2qLy4ukC'

class Captcha(object):
    '''
    Captcha class that represent a session.
    '''
    def __init__(self, domain, pub_key, pri_key):
        self.domain = domain
        self.pub_key = pub_key
        self.pri_key = pri_key
