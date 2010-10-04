#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework import encode

class Test(unittest.TestCase):

    def test_encode_html(self):
        self.assertEquals('abc', encode.encode_html('abc'))
        self.assertEquals('&lt;h1&gt;', encode.encode_html('<h1>'))
        self.assertEquals('A&amp;B&amp;C', encode.encode_html('A&B&C'))
        self.assertEquals('&quot;Hi!&quot;', encode.encode_html('"Hi!"'))

        self.assertEquals('abc', encode.encode_html(u'abc'))
        self.assertEquals('&lt;h1&gt;', encode.encode_html(u'<h1>'))
        self.assertEquals('A&amp;B&amp;C', encode.encode_html(u'A&B&C'))
        self.assertEquals('&quot;Hi!&quot;', encode.encode_html(u'"Hi!"'))

    def test_encode_json(self):
        self.assertEquals('abc', encode.encode_json('abc'))
        self.assertEquals(r'abc\r\nxyz', encode.encode_json('abc\r\nxyz'))
        self.assertEquals(r'hello, \"world\"', encode.encode_json('hello, "world"'))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
