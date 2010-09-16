#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework.web import Context

class Test(unittest.TestCase):

    def test_context_kw(self):
        ctx = Context(name='Michael', title='Engineer')
        self.assertEquals('Michael', ctx['name'])
        self.assertEquals('Michael', ctx.name)
        self.assertEquals('Engineer', ctx['title'])
        self.assertEquals('Engineer', ctx.title)
        self.assertRaises(AttributeError, lambda: ctx.url)
        ctx.url = 'http://www.expressme.org'
        self.assertEquals('http://www.expressme.org', ctx.url)

    def test_context_dict(self):
        ctx = Context({'name': 'Michael', 'title': 'Engineer'})
        self.assertEquals('Michael', ctx['name'])
        self.assertEquals('Michael', ctx.name)
        self.assertEquals('Engineer', ctx['title'])
        self.assertEquals('Engineer', ctx.title)

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
