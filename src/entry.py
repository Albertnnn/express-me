#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
ExpressMe web application entry point: mapping to r'^/.*$'.
'''

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from framework.web import Dispatcher

application = webapp.WSGIApplication([('^/.*$', Dispatcher)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
