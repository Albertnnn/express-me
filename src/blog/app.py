#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Blog app that display blog posts.
'''

from exweb import get
from exweb import post
from exweb import context
from exweb import HttpForbiddenError
from exweb import HttpNotFoundError

from manage import shared
from blog import store

def assert_not_none(o):
    if o is None:
        raise HttpNotFoundError()

@get('/')
def get_public_posts():
    '''
    show all public posts of blog
    '''
    return {
            'title' : 'Posts',
            'posts' : store.get_public_posts(),
            'feed' : __get_feed()
    }

@get('/p/$')
def get_posts_by_page(page):
    '''
    show public posts of blog at specified page.
    '''
    # FIXME: 
    return {
            'title' : 'Posts',
            'posts' : store.get_public_posts(),
            'feed' : __get_feed()
    }

@get('/tag/$')
def get_posts_by_tag(tag_key):
    tag = store.get_tag(tag_key)
    return {
            'title' : tag.tag_nicename,
            'tag' : tag,
            'posts' : get_posts_by_tag(tag),
            'feed' : __get_feed()
    }

@get('/cat/$')
def get_posts_by_category(cat_key):
    category = store.get_category(cat_key)
    return {
            'title' : category.category_name,
            'category' : category,
            'posts' : store.get_posts_by_category(category),
            'feed' : __get_feed()
    }

@get('/post/$')
def get_post(key):
    '''
    Show a single published post.
    
    Args:
        key: post key as string.
    '''
    p = store.get_post(key)
    assert_not_none(p)
    return {
            'title' : p.post_title,
            'post' : p,
            'comments' : shared.get_comments(key),
            'feed' : __get_feed()
    }

@get('/page/$')
def get_page(key):
    '''
    Show a single page.
    
    Args:
        key: page key as string.
    '''
    p = store.get_page(key)
    assert_not_none(p)
    return {
            'title' : p.post_title,
            'page' : p,
            'feed' : __get_feed()
    }

def __get_feed():
    ''' get feed url and title '''
    url = shared.get_setting('blog_setting', 'feed_proxy', '/blog/feed')
    title = shared.get_setting('blog_setting', 'feed_title', 'Rss Feed')
    return { 'url' : url, 'title' : title }

@post('/comment')
def make_comment():
    ''' make a comment on a post or page '''
    form = context.form
    id = form.get('id')
    post = store.get_post(id)
    if not post.comment_allow:
        raise HttpForbiddenError()
    ref = str(post.key())
    name = form.get('name', '')
    link = form.get('link', '')
    content = form.get('content')
    content = '<p>' + '</p><p>'.join(content.split('\n')) + '</p>'
    key = str(shared.create_comment(ref, content, name, link).key())
    return 'redirect:/blog/post/%s#%s' % (ref, key)

@get('/feed')
def feed():
    '''
    Generate rss feed.
    '''
    host = context.request.host_url
    title = shared.get_setting('blog_setting', 'feed_title', 'Rss Feed')
    description = shared.get_setting('blog_setting', 'feed_desc', 'Subscribe Rss Feed')
    hub = 'http://pubsubhubbub.appspot.com'
    link = 'http://feeds.feedburner.com/expressme'
    max = 20
    posts = store.get_posts(limit=max)
    response = context.response
    response.content_type = 'application/rss+xml'
    response.charset = 'utf8'
    out = response.out
    out.write(r'''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:slash="http://purl.org/rss/1.0/modules/slash/">
<channel><atom:link rel="hub" href="''')
    out.write(hub)
    out.write('"/><title>')
    out.write(title)
    out.write('</title><link>')
    out.write(link)
    out.write('</link><description>')
    out.write(description)
    out.write('</description><generator>expressme.org</generator><language>en</language>\n')
    for post in posts:
        out.write('<item><title>')
        out.write(post.post_title)
        out.write('</title><link>')
        out.write(host)
        out.write('/blog/post/')
        out.write(str(post.key()))
        out.write('</link><dc:creator>')
        out.write(post.post_owner.user_nicename)
        out.write('</dc:creator><pubDate>')
        out.write(__format_rss_date(post.post_date))
        out.write('</pubDate><description><![CDATA[')
        out.write(post.post_content)
        out.write(']]></description></item>\n')
    out.write('</channel></rss>')

def __format_rss_date(dt):
    # format: Sun, 07 Feb 2010 20:56:30
    return dt.strftime('%a, %d %b %Y %H:%M:%S')
