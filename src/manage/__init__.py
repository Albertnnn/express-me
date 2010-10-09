#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
app that do management.
'''

from time import time

import hashlib
import base64
import os

from framework import ApplicationError

def get_themes():
    root = os.path.split(os.path.dirname(__file__))[0]
    theme_root = os.path.join(root, 'theme')
    themes = os.listdir(theme_root)
    valid_themes = [theme for theme in themes if __is_valid_theme(theme_root, theme)]
    valid_themes.sort()
    return valid_themes

def __is_valid_theme(theme_root, theme):
    dir = os.path.join(theme_root, theme)
    file = os.path.join(dir, 'template.html')
    return os.path.isdir(dir) and os.path.isfile(file)
