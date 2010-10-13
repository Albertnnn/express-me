#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from google.appengine.ext import webapp
from framework.web import Dispatcher

import interceptor

class Test(unittest.TestCase):

    def init_get(self, url):
        self._init_http('GET', url)

    def init_post(self, url):
        self._init_http('POST', url)

    def _init_http(self, method, url):
        self.request = webapp.Request.blank(url, environ={'REQUEST_METHOD' : method})
        #self.request.set_status = lambda x: self.request.status
        self.response = webapp.Response() #webob.Response(request=self.request))
        self.dispatcher = Dispatcher()
        self.dispatcher.initialize(self.request, self.response)
        interceptor.intercept = lambda kw: None
        if method=='GET':
            self.dispatcher.get()
        else:
            self.dispatcher.post()

    def test_home(self):
        self.init_get('/http_test/')
        self.assertEquals('<h1>Home</h1>', self.response.out.getvalue())

    def test_hello(self):
        self.init_post('/http_test/hello/world')
        self.assertEquals('<p>Hello, world!</p>', self.response.out.getvalue())
        self.init_post('/http_test/hello/Michael')
        self.assertEquals('<p>Hello, Michael!</p>', self.response.out.getvalue())

    def test_mapping(self):
        self.init_get('/http_test/hi/Michael')
        self.assertEquals('<p>Hi, Michael!</p>', self.response.out.getvalue())
        self.init_post('/http_test/hi/Michael')
        self.assertEquals('<p>Hi, Michael!</p>', self.response.out.getvalue())

    def test_redirect(self):
        self.init_get('/http_test/redirect/abc')
        self.assertEquals('/about/abc', self.response.headers['Location'])

    def test_args(self):
        self.init_get('/http_test/args?q=Express%20Me&ref=&nl=en_US&nl=zh_CN')
        self.assertEquals(u'Express Me, , None, [en_US, zh_CN]', self.response.out.getvalue())

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
