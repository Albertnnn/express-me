#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from datetime import datetime
from datetime import timedelta

from framework import gaeunit
from manage import model

class Test(gaeunit.GaeTestCase):

    def test_gen_token(self):
        user_key = 'user-12345-USS-887700'
        tokens = []
        for i in range(100):
            token = model.create_reset_password_token(user_key)
            tokens.append(token)
        self.assertEquals(100, len(tokens))
        self.assertEquals(100, len(frozenset(tokens)))

    def test_delete_expired_token(self):
        user_key = 'user-12345-USS-887700'
        token1 = 'ABC_123_TTS'
        # token1 should be expired:
        t = model.ResetPasswordToken(ref=user_key, token=token1, creation_date=(datetime.now()-timedelta(3, 0)))
        t.put()
        self.assertEquals(None, model.get_reset_password_token(user_key))
        # token2 is valid:
        token2 = model.create_reset_password_token(user_key)
        self.assertEquals(token2, model.get_reset_password_token(user_key))
        # query all token (include invalid):
        all = model.ResetPasswordToken.all().filter('ref =', user_key).order('-creation_date').fetch(100)
        self.assertEquals(2, len(all))
        self.assertEquals(token2, all[0].token)
        self.assertEquals(token1, all[1].token)
        # delete expired token1:
        model.cron_delete_expired_token()
        all = model.ResetPasswordToken.all().filter('ref =', user_key).order('-creation_date').fetch(100)
        self.assertEquals(1, len(all))
        self.assertEquals(token2, all[0].token)

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
