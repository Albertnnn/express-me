#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Adsense Widget that display Google Adsense.
'''

import widget

class Widget(widget.WidgetModel):

    __title__ = 'Google AdSense'
    __description__ = 'Display A.D. of your Google AdSense account.'
    __author__ = 'Michael Liao'
    __url__ = 'http://www.expressme.org/'

    '''
    Display Google Adsense
    '''
    pub_id = widget.WidgetSetting(description='Publisher ID', required=True)
    ad_slot = widget.WidgetSetting(description='Ad. Slot', required=True)
    ad_width = widget.WidgetSetting(description='Ad. Width', required=True)
    ad_height = widget.WidgetSetting(description='Ad. Height', required=True)

    def get_content(self):
        if not self.pub_id:
            return '<p>error: missing pub_id</p>'
        if not self.ad_slot:
            return '<p>error: missing ad_slot</p>'
        if not self.ad_width:
            return '<p>error: missing ad_width</p>'
        if not self.ad_height:
            return '<p>error: missing ad_height</p>'
        return '''<!-- begin google adsense -->
<script type="text/javascript"><!--
google_ad_client = "%s";
google_ad_slot = "%s";
google_ad_width = %s;
google_ad_height = %s;
//-->
</script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
<!-- end google adsense -->
''' % (self.pub_id, self.ad_slot, self.ad_width, self.ad_height)
