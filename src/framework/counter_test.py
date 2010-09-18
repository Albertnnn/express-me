#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest
import threading

from framework import counter
from framework import gaeunit

class CounterThread(threading.Thread):
    '''
    Test thread for updating counter.
    '''
    def __init__(self, name, delta=1):
        super(CounterThread, self).__init__()
        self.name = name
        self.delta = delta

    def run(self):
        counter.incr(self.name, self.delta)

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
        name = 'multi'
        self.assertEquals(0, counter.get(name))
        ts = []
        for i in range(1, 10):
            ts.append(CounterThread(name, i))
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        self.assertEquals(1+2+3+4+5+6+7+8+9, counter.get(name))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
