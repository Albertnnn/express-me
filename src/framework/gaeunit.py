#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Base test case for Google AppEngine.
'''

import os
import sys
import unittest

def _lookup_gae_home():
    '''
    Return GAE home. Lookup order:
    1. Environment variable 'GAE_HOME'.
    2. Default path depends on OS.
    '''
    if 'GAE_HOME' in os.environ:
        return _check_or_raise(os.environ['GAE_HOME'])
    if os.name=='nt':
        return _check_or_raise(r'C:\Program Files\Google\google_appengine')
    if os.name=='posix':
        import getpass
        return _check_or_raise('/home/%s/google_appengine' % getpass.getuser())

def _get_extra_path(gae_home):
    return [
            gae_home,
            os.path.join(gae_home, 'google', 'appengine', 'api'),
            os.path.join(gae_home, 'google', 'appengine', 'ext'),
            os.path.join(gae_home, 'lib', 'yaml', 'lib'),
            os.path.join(gae_home, 'lib', 'webob'),
    ]

def _check_or_raise(path):
    if not os.path.isdir(path):
        raise IOError('GAE_HOME is undefined or invalid.')
    return path

# init GAE env here:
def init_once():
    gae_home = _lookup_gae_home()
    if not gae_home in sys.path:
        sys.path.extend(_get_extra_path(_lookup_gae_home()))

init_once()

class GaeTestCase(unittest.TestCase):
    '''
    Base GAE TestCase that prepare all GAE local environment for test.
    '''

    def setUp(self):
        super(GaeTestCase, self).setUp()

        from google.appengine.api import apiproxy_stub_map

        yaml = os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'app.yaml')
        appid = _get_app_id(yaml)
        _setup_env(appid)
        apiproxy_stub_map.apiproxy = _get_dev_apiproxy(appid)

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
    from google.appengine.api.memcache import memcache_stub

    apiproxy = apiproxy_stub_map.APIProxyStubMap()
    apiproxy.RegisterStub('datastore_v3', datastore_file_stub.DatastoreFileStub(appid, None, None))
    apiproxy.RegisterStub('user', user_service_stub.UserServiceStub())
    apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())
    apiproxy.RegisterStub('mail', mail_stub.MailServiceStub()) 
    apiproxy.RegisterStub('memcache', memcache_stub.MemcacheServiceStub())
    return apiproxy
