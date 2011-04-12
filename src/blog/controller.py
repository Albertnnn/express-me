#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Blog app that display blog posts.
'''

from framework.web import NotFoundError
from framework.web import get
from framework.web import post

from framework import store

import blog
from blog import model

@get('/')
def get_all_public_posts(**kw):
    '''
    show all public posts of blog
    '''
    ctx = kw['context']
    number = 20
    index = ctx.get_argument('index', '')
    if index:
        index = int(index)
    else:
        index = 1
    offset = ctx.get_argument('offset', '')
    if not offset:
        offset = None
    posts, next = model.get_posts(number, offset)
    return {
            '__theme__' : True,
            '__view__' : 'posts',
            '__title__' : 'All posts',
            '__header__' : blog.get_feed_html(),
            'posts' : posts,
            'index' : index,
            'next' : next,
            'offset' : offset,
    }

@get('/t/$')
def get_posts_by_tag(tag_key):
    tag = store.get_tag(tag_key)
    return {
            'title' : tag.tag_nicename,
            'tag' : tag,
            'posts' : get_posts_by_tag(tag),
            'feed' : blog_utils.get_feed()
    }

@get('/cat/$')
def get_posts_by_category(cat_key, **kw):
    ctx = kw['context']
    category = model.get_category(cat_key)
    number = 20
    offset = ctx.get_argument('offset', '')
    if not offset:
        offset = None
    index = ctx.get_argument('index', '')
    if index:
        index = int(index)
    else:
        index = 1
    posts, next = model.get_posts(number, offset, category=category)
    return {
            '__theme__' : True,
            '__view__' : 'posts',
            '__title__' : 'Posts of %s' % category.name,
            '__header__' : blog.get_feed_html(),
            'category' : category,
            'posts' : posts,
            'index' : index,
            'next' : next,
            'offset' : offset,
    }

@get('/post/$')
def get_post(key):
    '''
    Show a single published post.
    
    Args:
        key: post key as string.
    '''
    post = model.get_post(key)
    if post is None:
        raise NotFoundError()
    return {
            '__theme__' : True,
            '__view__' : 'post',
            '__title__' : post.title,
            'post' : post,
            'comments' : store.get_all_comments(post.id),
    }

@get('/page/$')
def get_page(key):
    '''
    Show a single page.
    
    Args:
        key: page key as string.
    '''
    page = model.get_post(key, True)
    if page is None:
        raise NotFoundError()
    return {
            '__theme__' : True,
            '__view__' : 'page',
            '__title__' : page.title,
            'page' : page,
    }

@post('/comment')
def comment():
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
def feed(**kw):
    '''
    Generate rss feed.
    '''
    host = kw['request'].host_url
    options = store.get_settings(blog.GROUP_OPTIONS)
    blog.update_default_settings(options)
    title = options[blog.FEED_TITLE]
    description = 'Subscribe RSS feed'
    hub = 'http://pubsubhubbub.appspot.com'
    link = options[blog.FEED_PROXY] or ('%s/blog/feed' % host)
    max = int(options[blog.FEED_ITEMS])
    posts, cursor = model.get_posts(limit=max)
    response = kw['response']
    response.content_type = 'application/rss+xml'
    response.charset = 'utf8'
    out = response.out
    out.write(r'''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:slash="http://purl.org/rss/1.0/modules/slash/">
  <channel>
    <atom:link rel="hub" href="%s"/>
    <title>%s</title>
    <link>%s</link>
    <description>%s</description>
    <generator>expressme.org</generator>
    <language>en</language>''' % (hub, title, link, description))
    for post in posts:
        out.write(r'''
    <item>
      <title>%s</title>
      <link>%s/blog/post/%s</link>
      <dc:creator>%s</dc:creator>
      <pubDate>%s</pubDate>
      <description><![CDATA[%s]]></description>
    </item>''' % (
            post.title,
            host,
            post.id,
            post.author,
            post.creation_date.strftime('%a, %d %b %Y %H:%M:%S'),
            post.content
    ))
    out.write(r'''
  </channel>
</rss>
''')
