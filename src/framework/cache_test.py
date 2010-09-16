#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework import cache
from framework import gaeunit

class Test(gaeunit.GaeTestCase):

    def test_cache(self):
        key1 = 'key1'
        key2 = 'key2'
        self.assertEquals(None, cache.get(key1))
        self.assertEquals(None, cache.get(key2))
        cache.set(key1, 'abc')
        cache.set(key2, 'xyz')
        self.assertEquals('abc', cache.get(key1))
        self.assertEquals('xyz', cache.get(key2))
        cache.delete(key1)
        cache.delete(key2)
        self.assertEquals(None, cache.get(key1))
        self.assertEquals(None, cache.get(key2))

    def test_incr(self):
        key = 'inc'
        self.assertEquals(None, cache.get(key))
        cache.set(key, 123)
        self.assertEquals(123, cache.get(key))
        cache.incr(key)
        self.assertEquals(124, cache.get(key))
        cache.incr(key, 10)
        self.assertEquals(134, cache.get(key))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
