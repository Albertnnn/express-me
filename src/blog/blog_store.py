#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEPRECATED = True

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

from google.appengine.ext import db

class BlogPostMeta(db.Model):
    'meta info for BlogPost'
    meta_key = db.StringProperty(required=True)
    meta_values = db.StringListProperty()

class BlogTag(db.Model):
    'a tag object'
    tag_name = db.StringProperty(required=True)
    tag_nicename = db.StringProperty(required=True)
    tag_count = db.IntegerProperty(required=True, default=0)

def get_tag(key):
    '''
    get tag object by key.
    
    Args:
        key: key of tag.
    Return: BlogTag object, or None if no such tag.
    '''
    return BlogTag.get(key)

def get_tags(limit=100):
    '''
    get tags order by tag name.
    
    Args:
        limit: maximum number of tags. default to 100.
    Returns: list of BlogTag objects.
    '''
    return BlogTag.all().order('tag_name').fetch(limit)

def get_hot_tags(limit=100):
    '''
    get hot tags.
    
    Args:
        limit: maximum number of tags. default to 100.
    Returns: list of BlogTag objects.
    '''
    return BlogTag.all().filter('tag_count >', 0).order('-tag_count').order('tag_name').fetch(limit)

def list_tags():
    return BlogTag.all().filter('tag_count >', 0).order('tag_name').fetch(1000)

def create_tag(nicename, increase=1):
    '''
    Create or update a tag. If tag is not exist, new tag will be created.
    
    Args:
        increase: increase of tag_count, default to 1.
    Returns:
        tag object.
    '''
    nicename = nicename.strip()
    name = nicename.lower()
    tag = BlogTag.all().filter('tag_name =', name).get()
    if tag is None:
        tag = BlogTag(tag_name=name, tag_nicename=nicename, tag_count=increase)
        tag.put()
    else:
        tag.tag_count += increase
        tag.put()
    return tag
