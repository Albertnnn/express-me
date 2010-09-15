#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Base test case for Google AppEngine.
'''

DEFAULT_GAE_HOME = '/home/michael/google_appengine'

import os
import sys
import unittest

class GaeTestCase(unittest.TestCase):
    '''
    Base GAE TestCase that prepare all GAE local environment for test.
    '''

    def __init__(self, *args, **kwargs):
        super(GaeTestCase, self).__init__(*args, **kwargs)
        gae_home = self.gae_home()
        sys.path = _get_extra_path(gae_home) + sys.path

        from google.appengine.api import apiproxy_stub_map

        yaml = os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'app.yaml')
        appid = _get_app_id(yaml)
        _setup_env(appid)
        apiproxy_stub_map.apiproxy = _get_dev_apiproxy(appid)

    def gae_home(self):
        '''
        Hook for getting GAE home.
        '''
        return DEFAULT_GAE_HOME

def _get_app_id(app_yaml_file):
    '''
    Get application id from yaml file.
    
    Args:
        app_yaml_file: full path of app.yaml file.
    
    Returns:
        appid as str.
    '''
    f = None
    try:
        f = open(app_yaml_file, 'r')
        for line in f:
            s = line.strip()
            if s.startswith('application:'):
                return s[12:].strip()
    finally:
        if f is not None:
            f.close()

def _get_extra_path(gae_home):
    return [
            gae_home,
            os.path.join(gae_home, 'google', 'appengine', 'api'),
            os.path.join(gae_home, 'google', 'appengine', 'ext'),
            os.path.join(gae_home, 'lib', 'yaml', 'lib'),
            os.path.join(gae_home, 'lib', 'webob'),
    ]

def _setup_env(appid):
    os.environ['APPLICATION_ID'] = appid
    os.environ['AUTH_DOMAIN'] = 'example.com'
    os.environ['USER_EMAIL'] = 'test@example.com'

def _get_dev_apiproxy(appid):
    from google.appengine.api import apiproxy_stub_map
    from google.appengine.api import datastore_file_stub
    from google.appengine.api import user_service_stub
    from google.appengine.api import mail_stub
    from google.appengine.api import urlfetch_stub

    apiproxy = apiproxy_stub_map.APIProxyStubMap()
    apiproxy.RegisterStub('datastore_v3', datastore_file_stub.DatastoreFileStub(appid, None, None))
    apiproxy.RegisterStub('user', user_service_stub.UserServiceStub())
    apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())
    apiproxy.RegisterStub('mail', mail_stub.MailServiceStub()) 
    return apiproxy
