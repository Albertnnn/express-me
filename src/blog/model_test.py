#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import time
import unittest

from framework.gaeunit import GaeTestCase
from framework import store
from blog import model

def _create_user():
    return store.create_user(store.ROLE_ADMINISTRATOR, 'test@email.com', 'password', 'Bob')

def _create_post(num, ref_user, title_prefix, tag, category, func_state=lambda x: model.POST_PUBLISHED):
    ' create number of posts '
    for i in range(num-1, -1, -1):
        model.create_post(
                ref_user,
                func_state(i),
                '%s-%d' % (title_prefix, i,),
                'just a test. no. %d' % i,
                category,
                tag,
                True
        )
        time.sleep(0.01)

class Test(GaeTestCase):

    def test_create_post(self):
        user = _create_user()
        p = model.create_post(user, model.POST_PUBLISHED, 'test post', 'test content', model.get_category(), 'aa,bb,cc', True)
        self.assertEquals(user.id, p.ref)
        self.assertEquals(user.nicename, p.author)
        p2 = model.get_post(p.id)
        self.assertEquals(user.id, p2.ref)
        self.assertEquals(user.nicename, p2.author)

    def test_get_posts_by_category(self):
        # prepare 20 posts:
        python = model.create_category('python')
        java = model.create_category('java')
        _create_post(10, _create_user(), 'python test', 'this is a python test', python)
        _create_post(10, _create_user(), 'java test', 'this is a java test', java)
        ps, cursor = model.get_posts(limit, cursor, category, published_only)

    def test_get_posts(self):
        # prepare 20 posts:
        category = model.create_category('get_all')
        _create_post(20, _create_user(), 'test', 'abc', category)
        # get first 5: test-0, ..., test-4
        posts, cursor = model.get_posts(5)
        self.assertEquals(['test-%d' % d for d in range(5)], [str(p.title) for p in posts])
        # get next 10: test-5, ..., test-14:
        posts, cursor = model.get_posts(10, cursor)
        self.assertEquals(['test-%d' % d for d in range(5, 15)], [str(p.title) for p in posts])
        # get next 5: test-15, ..., test-19:
        posts, cursor = model.get_posts(10, cursor)
        self.assertEquals(['test-%d' % d for d in range(15, 20)], [str(p.title) for p in posts])

    def test_get_published_posts(self):
        # prepare 20 posts:
        category = model.create_category('get_pub')
        def _get_state(n):
            if n % 2==0:
                return model.POST_PUBLISHED
            return model.POST_DRAFT
        _create_post(20, _create_user(), 'test', 'abc', category, _get_state)
        # get first 5: test-0, test-2, test-4, test-6, test-8
        posts, cursor = model.get_published_posts(5)
        self.assertEquals(['test-%d' % d for d in range(0, 9, 2)], [str(p.title) for p in posts])
        # get next 5: test-10, test-12, test-14, test-16, test-18:
        posts, cursor = model.get_published_posts(10, cursor)
        self.assertEquals(['test-%d' % d for d in range(10, 19, 2)], [str(p.title) for p in posts])

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
