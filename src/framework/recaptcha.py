#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Simple anti-bot API for Google reCaptcha service.
'''

import logging
import urllib

RECAPTCHA_URL = 'http://www.google.com/recaptcha/api/verify'

TEST_DOMAIN = 'localhost'
TEST_PUB_KEY = '6LeAOr0SAAAAALQX_KWv_JhJpXrHNE5Xo0Z-UJwe'
TEST_PRI_KEY = '6LeAOr0SAAAAAAftuAAf6hI7McUzejjY2qLy4ukC'

def _encode(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    return s

def get_public_key():
    return TEST_PUB_KEY

def get_private_key():
    return TEST_PRI_KEY

def verify_captcha(recaptcha_challenge_field, recaptcha_response_field, private_key, remote_ip):
    if not (recaptcha_challenge_field and recaptcha_response_field and private_key):
        return False, 'Invalid captcha data'
    params = urllib.urlencode ({
            'privatekey': _encode(private_key),
            'remoteip' :  _encode(remote_ip),
            'challenge':  _encode(recaptcha_challenge_field),
            'response' :  _encode(recaptcha_response_field),
    })
    f = None
    try:
        f = urllib.urlopen(RECAPTCHA_URL, params)
        resp = f.read()
        logging.info('Get recaptcha result: %s' % resp)
        if resp.splitlines()[0]=='true':
            return True, 'Correct captcha'
        return False, 'Incorrect captcha words'
    except:
        logging.exception('Error when open url: %s' % RECAPTCHA_URL)
        return False, 'Network error'
    finally:
        if f is not None:
            f.close()
