#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from google.appengine.ext import db as db

from framework.gaeunit import GaeTestCase
from framework.store import BaseModel

from blog import model

class Test(GaeTestCase):

    def test_raw_field(self):
        input = 'Howto & Style'
        m = TestModel(name=input)
        self.assertEquals(input, m.name)
        self.assertEquals(input, m.name__raw__)
        self.assertRaises(AttributeError, lambda: m.location)
        self.assertRaises(AttributeError, lambda: m.location__raw__)
        delta = m.creation_date - m.modified_date
        self.assertEquals(0, delta.days)
        self.assertEquals(0, delta.seconds)
        self.assertTrue(m.id is None)
        m.put()
        self.assertFalse(m.id is None)
        self.assertEquals(m.id, str(m.key()))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
