#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

import webob
from google.appengine.ext import webapp
from framework.web import Dispatcher

class Test(unittest.TestCase):

    def init_get(self, url):
        self._init_http('GET', url)

    def init_post(self, url):
        self._init_http('POST', url)

    def _init_http(self, method, url):
        self.request = webob.Request.blank(url, environ={'REQUEST_METHOD' : method})
        #self.request.set_status = lambda x: self.request.status
        self.response = webapp.Response() #webob.Response(request=self.request))
        self.dispatcher = Dispatcher()
        self.dispatcher.initialize(self.request, self.response)
        if method=='GET':
            self.dispatcher.get()
        else:
            self.dispatcher.post()

    def test_home(self):
        self.init_get('/httptest/')
        self.assertEquals('<h1>Home</h1>', self.response.out.getvalue())

    def test_hello(self):
        self.init_post('/httptest/hello/world')
        self.assertEquals('<p>Hello, world!</p>', self.response.out.getvalue())
        self.init_post('/httptest/hello/Michael')
        self.assertEquals('<p>Hello, Michael!</p>', self.response.out.getvalue())

    def test_redirect(self):
        self.init_get('/httptest/redirect/abc')
        self.assertEquals('/about/abc/get', self.response.headers['Location'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
