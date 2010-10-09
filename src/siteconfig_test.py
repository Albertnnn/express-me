#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

import siteconfig

class Test(unittest.TestCase):

    def test_set_site_settings(self):
        site = siteconfig.Site(title='TITLE', subtitle='SUBTITLE')
        self.assertEquals('TITLE', site.title)
        self.assertEquals('SUBTITLE', site.subtitle)
        self.assertRaises(AttributeError, lambda : site.not_exist_attr)

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
