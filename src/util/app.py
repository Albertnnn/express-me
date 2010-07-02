#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

import logging

from google.appengine.api import urlfetch
from google.appengine.runtime import apiproxy_errors
from google.appengine.api import memcache

from exweb import context
from exweb import raw_mapping
from exweb import HttpNotFoundError

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
MAX_AGE = '2592000' # 2592000s = 720h = 30d

IGNORE_HEADERS = frozenset([
    'set-cookie',
    'expires',
    'cache-control',
    # Ignore hop-by-hop headers
    'connection',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailers',
    'transfer-encoding',
    'upgrade'
])

@raw_mapping(r'\/proxy\/(.*)')
def proxy(url):
    '''
    Make a proxy call and write response to current http request.
    
    For example, a remote resource 'http://www.google.com/images/logo.gif' 
    can be proxied as '/util/proxy/http%3A%2F%2Fwww.google.com%2Fimages%2Flogo.gif'.
    
    Raw url can also work such as '/util/proxy/http://www.google.com/images/logo.gif'
    
    Host name can be encoded as 'www_google_com', so this also works: 
    '/util/proxy/http://www_google_com/images/logo.gif'
    
    Returns:
        None, and data was wrote to current http response before returning.
    '''
    if not (url.startswith('http://') or url.startwith('https://')):
        raise HttpNotFoundError()

    root_pos = url.find('/', 8)
    if root_pos==(-1):
        url = url.replace('_', '.')
    else:
        url = url[:root_pos].replace('_', '.') + url[root_pos:]

    cached_data = memcache.get(url)
    if cached_data is not None:
        logging.info('Got cached content for url fetch: %s' % url)
        __write_to_response(context.response, cached_data)
        return

    # get cache time:
    cached_time = 0
    cached_param = context.query.get('__cache__', '')
    if cached_param:
        cached_time = int(cached_param)

    # fetch url:
    fetch_headers = {
        'User-Agent' : USER_AGENT,
        'Accept' : '*/*',
        'Referer' : url
    }
    try:
        result = urlfetch.fetch(url, headers=fetch_headers, follow_redirects=False)
    except (urlfetch.Error, apiproxy_errors.Error):
        raise HttpNotFoundError()

    response = context.response
    response.set_status(result.status_code)

    if (result.status_code!=200):
        return

    # build cache object:
    buffer = []
    for key, value in result.headers.iteritems():
        if key.lower() not in IGNORE_HEADERS:
            response.headers[key] = value
            buffer.append(key + ': ' + value)
    if cached_time>0:
        response.headers['Cache-Control'] = 'max-age=' + str(cached_time)
        buffer.append('Cache-Control: max-age=' + str(cached_time))
    else:
        response.headers['Cache-Control'] = 'max-age=' + MAX_AGE
    buffer.append('\n')
    buffer.append(result.content)
    cached_data = '\n'.join(buffer)
    if cached_time>0:
        memcache.set(url, cached_data, cached_time)
        logging.info('Put cached content after url fetch: %s' % url)

    # write to context.response:
    response.out.write(result.content)

def __write_to_response(response, data):
    header, body = data.split('\n\n\n', 1)
    headers = header.split('\n')
    for h in headers:
        pos = h.index(':')
        response.headers[h[:pos]] = h[pos+1:]
    response.out.write(body)
