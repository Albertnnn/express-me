#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import os
import unittest

from framework import view

class Test(unittest.TestCase):

    def test_get_template_path(self):
        self.assertTrue(os.path.isfile(view.get_template_path('http_test', 'main')))
        self.assertTrue(os.path.isfile(view.get_template_path('http_test', 'rss', '.xml')))

    def test_compile_template(self):
        cls = view.compile_template('http_test', 'main')
        self.assertTrue(isinstance(cls, str))
        self.assertTrue(cls.find('CompiledTemplate')>=0)

    def test_import_compiled_template(self):
        self.assertEquals(None, view.import_compiled_template('http_test.undefined'))

    def test_render(self):
        model = {
                'title' : 'Life & Style',
        }
        self.assertRaises(view.RenderError, view.render, 'http_test', model)
        model['__view__'] = 'undefined'
        self.assertRaises(view.RenderError, view.render, 'http_test', model)
        model['__view__'] = 'main'
        t = str(view.render('http_test', model))
        self.assertTrue(t.find('<h1>Life &amp; Style</h1>')>=0)
        self.assertTrue(t.find('<p>Life & Style</p>')>=0)

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
