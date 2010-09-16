#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework import validator

class Test(unittest.TestCase):

    def test_check_email(self):
        valid_emails = (
                'askxuefeng@gmail.com',
                'michael.liao@liaoxuefeng.com',
                'michael-liao@liaoxuefeng.com',
                'michael_liao@liaoxuefeng.com',
                'vip@example.com.cn',
                'vip@example-example.com.cn',
                'vip@vip-vip.example-example.com',
                '99@1234567.com',
                'cc_@123-456.com.fr',
                u'me@example.com.fr',
        )
        invalid_emails = (
                'ABC@example.COM',
                'im@micro$oft.com',
                '55-@@example.com',
                'test@example.com.',
                'test@vip.vip.example.com.cn',
                'test(at)example.com',
                '@example.com',
                'test-user@cc',
                12345,
        )
        for email in valid_emails:
            self.assertEquals(None, validator.check_email(email))
        for email in invalid_emails:
            self.assertRaises(ValueError, lambda: validator.check_email(email))

    def check_password(self):
        self.assertEquals(None, validator.check_password(''))
        self.assertEquals(None, validator.check_password('01234567890123456789012345678901'))
        self.assertEquals(None, validator.check_password('012345678901234567890123456789aa'))
        self.assertEquals(None, validator.check_password('aaaaaaaaaa00abcdefffffabcdefffff'))
        self.assertEquals(None, validator.check_password(u'aaaaaaaaaa00abcdefffffabcdefffff'))
        self.assertRaises(ValueError, lambda: validator.check_password('', allow_empty=False))
        self.assertRaises(ValueError, lambda: validator.check_password('    '))
        self.assertRaises(ValueError, lambda: validator.check_password('012345678901234567890123456789'))
        self.assertRaises(ValueError, lambda: validator.check_password('AAaaaaaaaa00abcdefffffabcdefffff'))
        self.assertRaises(ValueError, lambda: validator.check_password('aaaaaaaaaa--abcdefffffabcdefffff'))

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
