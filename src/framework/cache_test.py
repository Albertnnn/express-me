#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework import cache

class Test(unittest.TestCase):

    def test_cache(self):
        key1 = 'key1'
        key2 = 'key2'
        self.assertEquals(None, cache.get(key1))
        self.assertEquals(None, cache.get(key2))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
