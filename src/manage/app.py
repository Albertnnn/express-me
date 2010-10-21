#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Core app.
'''

DEPRECATED = True

import os

from manage import shared

@post('/upload/$')
def upload(type):
    if context.user is None:
        raise HttpForbiddenError()
    # get photo service:
    provider = shared.get_setting('storage', 'photo_provider', '')
    if not provider:
        return __upload_result(403, '', '', 'You do not configure a photo provider. Go to "Setting", "Storage" to configure a photo provider.')
    settings = shared.get_settings('storage')
    prefix = provider[:-len('PhotoProvider')].replace('.', '_')
    kw = {}
    for key in settings:
        if key.startswith(prefix):
            k = key[len(prefix):]
            v = settings[key]
            if isinstance(k, unicode):
                k = k.encode('utf8')
            if isinstance(v, unicode):
                v = v.encode('utf8')
            kw[k] = v
    try:
        module_name = provider[:-len('.PhotoProvider')]
        mod = __import__(module_name, globals(), locals(), ['PhotoProvider'])
        payload = context.request.get('NewFile')
        url = mod.PhotoProvider.upload(payload, 'title', 'upload from ExpressMe', **kw)
        if 'photo_proxied' in settings and settings['photo_proxied']=='True':
            import util
            url = util.make_proxy(url)
        __upload_result(0, url, 'filename', '')
    except Exception, e:
        __upload_result(1, '', 'filename', 'Upload failed: %s' % str(e))

def __upload_result(err, url, filename, msg):
    resp = '''
    <script type="text/javascript">
    (function(){
      var d=document.domain;
      while (true){
        try{
          var A=window.parent.document.domain;
          break;
        }
        catch(e) {};
        d=d.replace(/.*?(?:\.|$)/,'');
        if (d.length==0) break;
        try{document.domain=d;}
        catch (e){break;}
        }})();
    window.parent.OnUploadCompleted(%d, "%s", "%s", "%s");
    </script>
    ''' % (err, url, filename, msg)
    context.response.out.write(resp)
