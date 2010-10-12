#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

from datetime import datetime
import unittest

import runtime

class Test(unittest.TestCase):

    def test_format_datetime(self):
        # naive datetime, UTC as default:
        dt = datetime(2008, 2, 21, 5, 30, 59)
        # timezone +8:00, -8:00
        tz1 = runtime.UserTimeZone('UTC+8:00', 8, 0, 0)
        tz2 = runtime.UserTimeZone('UTC-8:00', -8, 0, 0)
        # format with tzinfo:
        self.assertEquals('2008-02-21 13:30:59', runtime.format_datetime(dt, tz1, '%Y-%m-%d %H:%M:%S'))
        self.assertEquals('2008-02-20 21:30:59', runtime.format_datetime(dt, tz2, '%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
