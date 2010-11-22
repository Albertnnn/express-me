#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import unittest

from framework.gaeunit import GaeTestCase
from widget import model

class Test(GaeTestCase):

    def test_get_installed_widgets(self):
        classes = model.get_installed_widgets()
        keys = classes.keys()
        fullnames = [classes[key].__module__[len('widget.installed.'):] for key in keys]
        fullnames.sort()
        self.assertEquals(['adsense', 'html', 'music_player', 'recent_tweets', 'subscribe'], fullnames)

    def test_load_widget_class(self):
        cls = model.load_widget_class('adsense')
        from widget.installed.adsense import Widget as w
        self.assertEquals(w, cls)

    def test_get_widget_instances(self):
        model.create_widget_instance('adsense', 0)
        model.create_widget_instance('html', 0)
        instances = model.get_widget_instances(0, False)
        self.assertEquals(2, len(instances))

        self.assertEquals('adsense', instances[0].name)
        self.assertEquals(0, instances[0].sidebar)
        self.assertEquals(0, instances[0].display_order)

        self.assertEquals('html', instances[1].name)
        self.assertEquals(0, instances[1].sidebar)
        self.assertEquals(1, instances[1].display_order)

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
