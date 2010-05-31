#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Music Widget that play music online.
'''

import widget

class Widget(widget.WidgetModel):

    widget_name = 'Music Player'
    widget_author = 'Michael Liao'
    widget_description = 'Play music online'
    widget_url = 'http://michael.liaoxuefeng.com/'

    '''
    Play music
    '''
    music_title = widget.WidgetSetting(description='Music Title', required=False, default='')
    music_url = widget.WidgetSetting(description='Music URL', required=True, default='http://')
    auto_play = widget.WidgetCheckedSetting(label='Auto play when load', description='Auto play', default='True')
    repeat = widget.WidgetCheckedSetting(label='Play repeatly', description='Play repeatly', default='False')

    def get_content(self):
        # http://shop.zzaza.com/content/mp3/burning.mp3
        # http://listen.idj.126.net/uf/130/40ef517cda864fc98886a26f7c01caa2.mp3
        auto_start = self.auto_play=='True'
        return r'''
<div>%s</div>
<div><embed src="/widget/installed/music_player/static/player.swf?soundFile=%s&playerID=%s&bg=0xf8f8f8&leftbg=0xeeeeee&lefticon=0x666666&rightbg=0xcccccc&rightbghover=0x999999&righticon=0x666666&righticonhover=0xffffff&text=0x666666&slider=0x666666&track=0xFFFFFF&border=0x666666&loader=0x9FFFB8&loop=no&autostart=%s" type="application/x-shockwave-flash" wmode="transparent" height="24" width="100%%" /></div>
''' % (self.music_title, self.music_url, self.__id__, auto_start)
