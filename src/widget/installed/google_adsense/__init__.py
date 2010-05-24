#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Adsense Widget that display Google Adsense.
'''

import widget

title = 'Google Adsense'
description = 'Display Google Adsense of specified account'

class Widget(widget.WidgetModel):
    '''
    Display Google Adsense
    '''

#    pub_id = widget.WidgetSetting()
#    ad_slot = widget.WidgetSetting()
#    ad_width = widget.WidgetSetting()
#    ad_height = widget.WidgetSetting()

    def load(self):
        self.pub_id = 'pub-6727358730461554'
        self.ad_slot = '2474475965'
        self.ad_width = '200'
        self.ad_height = '200'
        html = '''<!-- begin google adsense -->
<script type="text/javascript"><!--
google_ad_client = "%s";
google_ad_slot = "%s";
google_ad_width = %s;
google_ad_height = %s;
//-->
</script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
<!-- end google adsense -->
'''
        return {
                'title' : 'Google Adsense',
                'content' : html % (self.pub_id, self.ad_slot, self.ad_width, self.ad_height)
        }
