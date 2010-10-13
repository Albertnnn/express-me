#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest
import threading

from framework import gaeunit
from framework import store

class CounterThread(threading.Thread):
    '''
    Test thread for updating counter.
    '''
    def __init__(self, name, delta=1):
        super(CounterThread, self).__init__()
        self.name = name
        self.delta = delta

    def run(self):
        store.incr_count(self.name, self.delta)

class Test(gaeunit.GaeTestCase):

    def test_new_counter(self):
        name = 'test'
        self.assertEquals(0, store.get_count(name))
        for i in range(10):
            store.incr_count(name)
        self.assertEquals(10, store.get_count(name))
        for i in range(10):
            store.incr_count(name, 100)
        self.assertEquals(1010, store.get_count(name))

    def test_incr_shards(self):
        name = 'incr'
        self.assertEquals(0, store.get_count(name))
        for i in range(10):
            store.incr_count(name)
        store.incr_counter_shards(name, 100)
        self.assertEquals(10, store.get_count(name))
        for i in range(10):
            store.incr_count(name, 100)
        self.assertEquals(1010, store.get_count(name))

    def test_multithreads(self):
        name = 'multi'
        self.assertEquals(0, store.get_count(name))
        ts = []
        for i in range(1, 10):
            ts.append(CounterThread(name, i))
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        self.assertEquals(1+2+3+4+5+6+7+8+9, store.get_count(name))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
