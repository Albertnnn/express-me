#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework.web import _matches
from framework.web import get
from framework.web import post
from framework.web import raw_mapping

@get('/say')
def say():
    return 'hello'

@get('/product')
def get_product():
    return 'product'

@post('/create_order')
def create_order():
    return 'order'

@get('/$/$')
def get_category(manufacturer, category):
    return '%s,%s' % (manufacturer, category)

@raw_mapping('/(.+)/([0-9]+)')
def save_category(name, id):
    return '%s-%s' % (name, id)

class Test(unittest.TestCase):

    def test_matches(self):
        # matched, not raw mapping:
        self.assertEquals((), _matches('/', False, '/'))
        self.assertEquals((), _matches('/abc', False, '/abc'))
        self.assertEquals((), _matches('/a/b/c', False, '/a/b/c'))
        self.assertEquals((), _matches('/a/', False, '/a/'))

        self.assertEquals(('123',), _matches('/$', False, '/123'))
        self.assertEquals(('abc',), _matches('/$', False, '/abc'))
        self.assertEquals(('xyz',), _matches('/$/', False, '/xyz/'))
        self.assertEquals(('a', 'b', 'c'), _matches('/$/$/$/', False, '/a/b/c/'))
        self.assertEquals(('a', 'b', 'c'), _matches('/$-$-$/', False, '/a-b-c/'))
        self.assertEquals(('a', 'b', 'c'), _matches('/pro-$/$/$/', False, '/pro-a/b/c/'))

        # not matched, not raw mapping:
        self.assertEquals(None, _matches('/', False, ''))
        self.assertEquals(None, _matches('/', False, '/abc'))
        self.assertEquals(None, _matches('/$', False, '/abc/'))
        self.assertEquals(None, _matches('/$/$/', False, '/a/b/c/'))
        self.assertEquals(None, _matches('/abc-$', False, '/abc.xyz'))

        # matched, raw mapping:
        self.assertEquals((), _matches('/', True, '/'))
        self.assertEquals(('abc',), _matches('/(.*)', True, '/abc'))
        self.assertEquals(('abc/xyz',), _matches('/(.*)', True, '/abc/xyz'))
        self.assertEquals(('abc', 'xyz'), _matches('/(.*)/(.*)', True, '/abc/xyz'))
        self.assertEquals(('a', 'b', ''), _matches('/(.+)/(.+)/(.*)', True, '/a/b/'))

        # not matched, raw mapping:
        self.assertEquals(None, _matches('/', True, ''))
        self.assertEquals(None, _matches('/abc(.+)', True, '/abc'))
        self.assertEquals(None, _matches('/(.+)/(.+)/(.+)', True, '/a/b/'))

    def test_say(self):
        f = say
        self.assertTrue(f.support_get)
        self.assertFalse(f.support_post)
        self.assertFalse(f.raw_mapping)
        self.assertEquals('/say', f.pattern)
        self.assertEquals('say', f.__name__)
        self.assertEquals('hello', f())
        self.assertEquals((), f.matches('/say'))
        self.assertEquals(None, f.matches('/say/'))

    def test_get_product(self):
        f = get_product
        self.assertTrue(f.support_get)
        self.assertFalse(f.support_post)
        self.assertFalse(f.raw_mapping)
        self.assertEquals('/product', f.pattern)
        self.assertEquals('get_product', f.__name__)
        self.assertEquals('product', f())
        self.assertEquals((), f.matches('/product'))
        self.assertEquals(None, f.matches('/product/'))

    def test_create_order(self):
        f = create_order
        self.assertFalse(f.support_get)
        self.assertTrue(f.support_post)
        self.assertFalse(f.raw_mapping)
        self.assertEquals('/create_order', f.pattern)
        self.assertEquals('create_order', f.__name__)
        self.assertEquals('order', f())
        self.assertEquals((), f.matches('/create_order'))
        self.assertEquals(None, f.matches('/create_order/'))

    def test_get_category(self):
        f = get_category
        self.assertTrue(f.support_get)
        self.assertFalse(f.support_post)
        self.assertFalse(f.raw_mapping)
        self.assertEquals('/$/$', f.pattern)
        self.assertEquals('a,b', f('a', 'b'))
        self.assertEquals('get_category', f.__name__)
        self.assertEquals(('a', 'b'), f.matches('/a/b'))
        self.assertEquals(None, f.matches('/a/b/'))

    def test_save_category(self):
        f = save_category
        self.assertTrue(f.support_get)
        self.assertTrue(f.support_post)
        self.assertTrue(f.raw_mapping)
        self.assertEquals('/(.+)/([0-9]+)', f.pattern)
        self.assertEquals('a-b', f('a', 'b'))
        self.assertEquals('save_category', f.__name__)
        self.assertEquals(('a', '123'), f.matches('/a/123'))
        self.assertEquals(None, f.matches('/a/b'))
        self.assertEquals(None, f.matches('//123'))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
