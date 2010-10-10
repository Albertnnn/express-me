#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

from datetime import datetime
import unittest

import siteconfig

class Test(unittest.TestCase):

    def test_date_format_samples(self):
        dt = datetime(2008, 2, 21)
        self.assertEquals([
                ('%Y-%m-%d', '2008-02-21'),
                ('%y-%m-%d', '08-02-21'),
                ('%d/%m/%Y', '21/02/2008'),
                ('%d/%m/%y', '21/02/08'),
                ('%m/%d/%Y', '02/21/2008'),
                ('%m/%d/%y', '02/21/08'),
                ('%b %d, %Y', 'Feb 21, 2008'),
                ('%b %d, %y', 'Feb 21, 08'),
                ('%B %d, %Y', 'February 21, 2008'),
                ('%B %d, %y', 'February 21, 08'),
        ], siteconfig.date_format_samples(dt))

    def test_time_format_samples(self):
        dt = datetime(2008, 2, 21, 13, 20, 59)
        self.assertEquals([
                ('%H:%M:%S', '13:20:59'),
                ('%H:%M', '13:20'),
                ('%I:%M:%S %p', '01:20:59 PM'),
                ('%I:%M %p', '01:20 PM'),
        ], siteconfig.time_format_samples(dt))

    def test_default_setting(self):
        site = siteconfig.Site()
        self.assertEquals(siteconfig.DEFAULT_DATE, site.date_format)
        self.assertEquals(siteconfig.DEFAULT_TIME, site.time_format)
        self.assertEquals('ExpressMe', site.title)

    def test_set_site_settings(self):
        site = siteconfig.Site(title='TITLE', subtitle='SUBTITLE')
        self.assertEquals('TITLE', site.title)
        self.assertEquals('SUBTITLE', site.subtitle)
        self.assertRaises(AttributeError, lambda : site.not_exist_attr)

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
