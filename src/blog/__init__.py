#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

from google.appengine.ext import db
from manage import User

from exweb import HttpNotFoundError

class BlogPostMeta(db.Model):
    'meta info for BlogPost'
    meta_key = db.StringProperty(required=True)
    meta_values = db.StringListProperty()

# post state constants:

POST_STATE_PUBLISHED = 0
POST_STATE_PENDING = 1
POST_STATE_DRAFT = 2

class BlogTag(db.Model):
    'a tag object'
    tag_name = db.StringProperty(required=True)
    tag_nicename = db.StringProperty(required=True)
    tag_count = db.IntegerProperty(required=True, default=0)

class BlogCategory(db.Model):
    'a category object'
    category_name = db.StringProperty(required=True)
    category_description = db.StringProperty(required=False, default='', indexed=False)
    category_count = db.IntegerProperty(required=True, default=0, indexed=False)

class BlogPost(db.Model):
    'a single post'
    post_owner = db.ReferenceProperty(reference_class=User, required=True)
    post_state = db.IntegerProperty(required=True, default=POST_STATE_PUBLISHED)
    post_title = db.StringProperty(required=True)
    post_excerpt = db.TextProperty()
    post_content = db.TextProperty()
    post_category = db.ReferenceProperty(reference_class=BlogCategory)
    post_tags = db.StringListProperty()
    post_date = db.DateTimeProperty(auto_now_add=True)
    post_modified = db.DateTimeProperty(auto_now=True)
    post_static = db.BooleanProperty(default=False)
    comment_allow = db.BooleanProperty(required=True, default=True)
    comment_count = db.IntegerProperty(required=True, default=0)

    def post_tags_as_string(self):
        return ','.join(self.post_tags)

def get_hot_tags(limit=100):
    return BlogTag.all().filter('tag_count >', 0).order('-tag_count').order('tag_name').fetch(limit)

def list_tags():
    return BlogTag.all().filter('tag_count >', 0).order('tag_name').fetch(1000)

def create_post():
    pass

def get_post(key):
    p = BlogPost.get(key)
    if p is None or p.post_static:
        raise HttpNotFoundError()
    return p

def get_page(key):
    p = BlogPost.get(key)
    if p is None or not p.post_static:
        raise HttpNotFoundError()
    return p

def get_pages():
    return BlogPost.all().filter('post_static =', True).order('-post_date').fetch(1000)

def get_posts(date=None, limit=21):
    query = BlogPost.all()
    if date is not None:
        query = query.filter('post_date <=', date)
    return query.filter('post_static =', False).order('-post_date').fetch(limit)

def get_tags():
    return BlogTag.all().fetch(1000)

def get_category(key=None):
    '''
    Get category by key. if key is None, return the first category.
    '''
    if key is None:
        return get_categories()[0]
    return BlogCategory.get(key)

def get_categories():
    '''
    Get all categories.
    '''
    categories = BlogCategory.all().order('category_name').fetch(100)
    if not categories:
        cat = create_category('Uncategorized')
        categories.append(cat)
    return categories

def create_category(name, description='', count=0):
    '''
    Create a new category.
    
    Args:
        name: category name. NOTE that different categories may have same name.
        description: category description, default to ''.
    Returns:
        New category that created.
    Raises:
        MaximumNumberExceededError: if categories reach the maximum allowed number (100).
    '''
    if BlogCategory.all().count(100)==100:
        raise StandardError('Maximum number (100) of categories exceeded.')
    cat = BlogCategory(category_name=name, category_description=description, category_count=count)
    cat.put()
    return cat

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
