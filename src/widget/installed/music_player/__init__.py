#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Music Widget that play music online.
'''

import widget

name = 'Music Player'
author = 'Michael Liao'
description = 'Play MP3 online'
url = 'http://michael.liaoxuefeng.com/'

class Widget(widget.WidgetModel):
    '''
    Play music
    '''

#    music_url = widget.WidgetSetting()
#    auto_play = widget.WidgetSetting()
#    repeat = widget.WidgetSetting()

    def load(self):
        self.music_url = 'http://shop.zzaza.com/content/mp3/burning.mp3' #'http://listen.idj.126.net/uf/130/40ef517cda864fc98886a26f7c01caa2.mp3'
        self.music_title = 'Burning'
        self.auto_start = 'no'
        self.repeat = '0'
        html = r'<div>%s</div><div><embed src="/widget/music_box/static/player.swf?soundFile=%s&playerID=10&bg=0xf8f8f8&leftbg=0xeeeeee&lefticon=0x666666&rightbg=0xcccccc&rightbghover=0x999999&righticon=0x666666&righticonhover=0xffffff&text=0x666666&slider=0x666666&track=0xFFFFFF&border=0x666666&loader=0x9FFFB8&loop=no&autostart=%s" type="application/x-shockwave-flash" wmode="transparent" height="40" width="100%%" /></div>'
        return {
                'title' : 'Music Box',
                'content' : html % (self.music_title, self.music_url, self.auto_start)
        }
