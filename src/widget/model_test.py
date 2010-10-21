#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework.gaeunit import GaeTestCase
from widget import model

class Test(GaeTestCase):

    def test_get_installed_widgets(self):
        classes = model.get_installed_widgets()
        fullnames = [cls.__module__[len('widget.installed.'):] for cls in classes]
        self.assertEquals(['adsense', 'html', 'music_player', 'recent_tweets', 'subscribe'], fullnames)

    def test_load_widget_class(self):
        cls = model.load_widget_class('adsense')
        from widget.installed.adsense import Widget as w
        self.assertEquals(w, cls)

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
