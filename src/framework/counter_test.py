#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework import counter
from framework import gaeunit

class Test(gaeunit.GaeTestCase):

    def test_new_counter(self):
        name = 'test'
        self.assertEquals(0, counter.get(name))
        for i in range(10):
            counter.incr(name)
        self.assertEquals(10, counter.get(name))
        for i in range(10):
            counter.incr(name, 100)
        self.assertEquals(1010, counter.get(name))

    def test_incr_shards(self):
        name = 'incr'
        self.assertEquals(0, counter.get(name))
        for i in range(10):
            counter.incr(name)
        counter.incr_shards(name, 100)
        self.assertEquals(10, counter.get(name))
        for i in range(10):
            counter.incr(name, 100)
        self.assertEquals(1010, counter.get(name))

    def test_multithreads(self):
        pass

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
