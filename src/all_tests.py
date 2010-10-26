#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import os
import unittest

# import gaeunit to initialize GAE test environment:
import framework.gaeunit

def _search_tests(path, package, depth):
    all = os.listdir(path)
    prefix = package
    if package!='':
        prefix = package + '.'
    tests = ['%s%s' % (prefix, f[:-3]) for f in all if f.endswith('test.py')]
    L = []
    L.extend(tests)
    if depth<3:
        dirs = [d for d in all if os.path.isdir(os.path.join(path, d))]
        for d in dirs:
            L.extend(_search_tests(os.path.join(path, d), '%s%s' % (prefix, d), depth + 1))
    return L

if __name__ == '__main__':
    pwd = os.path.split(os.path.abspath(__file__))[0]
    tests = _search_tests(pwd, '', 0)
    suites = [unittest.defaultTestLoader.loadTestsFromName(test) for test in tests]
    unittest.TextTestRunner().run(unittest.TestSuite(suites))
