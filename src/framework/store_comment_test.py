#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework import ValidationError
from framework.gaeunit import GaeTestCase
from framework import store

class Test(GaeTestCase):

    def test_create_comment(self):
        ref = 'key123456789'
        email = 'guest@example.com'
        c = store.create_comment(ref, email, 'Guest', 'Hello!', '127.0.0.1', True)
        self.assertTrue(c.approval)
        c = store.create_comment(ref, email, 'Guest', 'Hi!', '127.0.0.1', False)
        self.assertFalse(c.approval)

    def test_get_comments(self):
        ref = 'key-ABC-999-KDE-010-USS'
        email = 'guest-%s@example.com'
        for i in range(10):
            store.create_comment(ref, email % i, 'Guest-%s' % i, 'No. %s' % i, '127.0.0.1', True)
        all = store.get_all_comments(ref)
        self.assertEquals(10, len(all))
        for i in range(10):
            self.assertEquals(email % i, all[i].email)

    def test_delete_comment(self):
        ref = 'NCC-74656'
        email = 'guest@example.com'
        c = store.create_comment(ref, email, 'Guest', 'Hello!', '127.0.0.1', True)
        self.assertEquals(email, c.email)
        # delete by reference key:
        store.delete_all_comments(ref)
        # comment still here:
        cs = store.get_all_comments(ref)
        self.assertEquals(1, len(cs))
        self.assertEquals(c.id, cs[0].id)
        # cron-delete is a real deletion:
        store.cron_delete_all_comments(ref)
        self.assertEquals(0, len(store.get_all_comments(ref)))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
