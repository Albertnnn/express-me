#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import hashlib
import unittest

from framework import ValidationError
from framework.gaeunit import GaeTestCase
from framework import store

class Test(GaeTestCase):

    def test_create_and_get_user(self):
        email = 'admin@expressme.org'
        password = hashlib.md5('admin-password').hexdigest()
        nicename = 'Admin'
        admin = store.create_user(store.ROLE_ADMINISTRATOR, email, password, nicename)
        self.assertFalse(admin is None)
        self.assertEquals(store.ROLE_ADMINISTRATOR, admin.role)
        self.assertEquals(email, admin.email)
        self.assertEquals(password, admin.password)
        self.assertEquals(nicename, admin.nicename)
        # get by email:
        u = store.get_user_by_email(email)
        self.assertFalse(u is None)
        self.assertEquals(store.ROLE_ADMINISTRATOR, u.role)
        self.assertEquals(email, u.email)
        self.assertEquals(password, u.password)
        self.assertEquals(nicename, u.nicename)
        # get by key:
        u = store.get_user_by_key(admin.id)
        self.assertFalse(u is None)
        self.assertEquals(store.ROLE_ADMINISTRATOR, u.role)
        self.assertEquals(email, u.email)
        self.assertEquals(password, u.password)
        self.assertEquals(nicename, u.nicename)
        # load non-exist user:
        u = store.get_user_by_email('nobody@expressme.org')
        self.assertTrue(u is None)

    def test_create_duplicate_users(self):
        email = 'howto@expressme.org'
        password = hashlib.md5('random-password').hexdigest()
        bob1 = store.create_user(store.ROLE_EDITOR, email, password, 'Bob1')
        self.assertFalse(bob1 is None)
        func = lambda: store.create_user(store.ROLE_CONTRIBUTOR, email, password, 'Bob2')
        self.assertRaises(ValidationError, func)
        self.assertRaises(ValidationError, func)
        # get by email, should be only one: Bob1
        us = store.User.all().filter('email =', email).fetch(100)
        self.assertEquals(1, len(us))
        u = store.get_user_by_email(email)
        self.assertEquals(store.ROLE_EDITOR, u.role)
        self.assertEquals(email, u.email)
        self.assertEquals('Bob1', u.nicename)

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
