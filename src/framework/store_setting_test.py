#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework.gaeunit import GaeTestCase
from framework import store

class Test(GaeTestCase):

    def test_set_setting(self):
        name = 'email'
        value = 'guest@example.com'
        self.assertTrue(store.get_setting(name) is None)
        self.assertEquals('default@default.com', store.get_setting(name, store.DEFAULT_GROUP, 'default@default.com'))
        store.set_setting(name, value)
        self.assertEquals(value, store.get_setting(name))
        name2 = 'url'
        value2 = 'http://guest.example.com'
        store.set_setting(name2, value2)
        # get settings as dict:
        d = store.get_settings()
        self.assertTrue(name in d)
        self.assertTrue(name2 in d)
        self.assertEquals(value, d[name])
        self.assertEquals(value2, d[name2])

    def test_error(self):
        self.assertRaises(ValueError, lambda: store.set_setting(123, 'abc'))
        self.assertRaises(ValueError, lambda: store.set_setting('abc', 123))
        self.assertRaises(ValueError, lambda: store.get_setting(123))
        self.assertRaises(ValueError, lambda: store.get_settings(9.99))

    def test_delete_setting(self):
        name = 'spaceship'
        value = 'NCC-74656'
        group = 'USS'
        store.set_setting(name, value, group)
        self.assertEquals('', store.get_setting(name, 'NON-USS', ''))
        self.assertEquals(value, store.get_setting(name, group, ''))
        store.delete_setting(name, group)
        self.assertEquals(None, store.get_setting(name, group))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
