#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

from google.appengine.ext import db

from framework import store
from framework import ApplicationError

# post state constants:

POST_PUBLISHED = 0
POST_PENDING = 1
POST_DRAFT = 2

CATEGORY_UNCATEGORIED = 'Uncategorized'

class BlogTag(db.Model):
    '''
    a tag object
    '''
    name = db.StringProperty(required=True)
    nicename = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True, default=0)

class BlogCategory(store.BaseModel):
    '''
    A blog category object
    '''
    name = db.StringProperty(required=True)
    description = db.StringProperty(required=False, default='', indexed=False)

class BlogPost(store.BaseModel):
    '''
    A single post
    '''
    ref = db.StringProperty(required=True) # user's key
    state = db.IntegerProperty(required=True, default=POST_PUBLISHED)
    title = db.StringProperty(required=True)
    excerpt = db.TextProperty(required=True)
    content = db.TextProperty(required=True)
    category = db.ReferenceProperty(required=True, reference_class=BlogCategory)
    tags = db.StringListProperty()
    static = db.BooleanProperty(default=False)
    allow_comment = db.BooleanProperty(required=True, default=True)

    def tags_as_string(self):
        return ','.join(self.post_tags)

def _query_posts(limit, cursor, ref_user=None, state=None, static=None, category=None, tag=None, order='-creation_date'):
    '''
    Low-level query with specific limit, cursor, filter and order.
    
    Returns:
        Query result as list and a cursor for next start of query.
    '''
    q = BlogPost.all()
    if ref_user is not None:
        q = q.filter('ref =', ref_user)
    if state is not None:
        q = q.filter('state =', state)
    if static is not None:
        q = q.filter('static =', static)
    if category is not None:
        q = q.filter('category =', category)
    if tag is not None:
        q = q.filter('tags =', tag)
    q = q.order(order)
    if cursor is not None:
        q.with_cursor(cursor)
    result = q.fetch(limit)
    return result, q.cursor()

def get_all_posts(limit=50, cursor=None):
    '''
    Get all posts with specific condition satisfied.
    
    Args:
        limit: maximum number of posts returned, default to 50.
        cursor: the last position of query.
    Returns:
        Posts list and a cursor to indicate the next position.
    '''
    return _query_posts(limit, cursor, static=False)

def get_published_posts(limit=50, cursor=None):
    '''
    Get all published posts with specific condition satisfied.
    
    Args:
        limit: maximum number of posts returned, default to 50.
        cursor: the last position of query.
    Returns:
        Posts list and a cursor to indicate the next position.
    '''
    return _query_posts(limit, cursor, state=POST_PUBLISHED, static=False)

def get_posts_by_tag(tag, limit=50, cursor=None):
    '''
    get all posts by tag.
    
    Args:
        tag: Tag object, or tag string.
        limit: Maximum return number.
    Return:
        Posts list and a cursor to indicate the next position.
    '''
    if isinstance(tag, BlogTag):
        tag = tag.tag_name
    else:
        tag = tag.lower()
    return _query_posts(limit, cursor, state=POST_PUBLISHED, static=False, tag=tag)

def get_posts_by_category(category, limit=50, cursor=None, published_only=True):
    '''
    get all posts by category.
    '''
    if published_only:
        return _query_posts(limit, cursor, state=POST_PUBLISHED, static=False, category=category)
    else:
        return _query_posts(limit, cursor, static=False, category=category)

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

def create_category(name, description=''):
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
        raise ApplicationError('Maximum number (100) of categories exceeded.')
    cat = BlogCategory(category_name=name, category_description=description, category_count=0)
    cat.put()
    return cat

def get_category(key=None):
    '''
    Get category by key. if key is None, return the first category.
    
    Args:
        key: key of category.
    Return: BlogCategory object, or None if no such category.
    '''
    if key is None:
        return get_categories()[0]
    return BlogCategory.get(key)

def get_categories():
    '''
    Get all categories as list.
    
    Returns: list of BlogCategory objects.
    '''
    categories = BlogCategory.all().order('category_name').fetch(100)
    if not categories:
        categories.append(create_category('Uncategorized'))
    return categories

def get_post(key, publish_only=True):
    '''
    get BlogPost by key.
    
    Args:
        key: key of post.
        publish_only: if post is published.
    Return: BlogPost object, or None if no such post.
    '''
    p = BlogPost.get(key)
    if p is None or p.static:
        return None
    if publish_only and p.state!=POST_PUBLISHED:
        return None
    return p

def get_page(key, publish_only=True):
    '''
    get BlogPost as static page by key.
    
    Args:
        key: key of post.
        publish_only: if post is published.
    Return: BlogPost object, or None if no such post.
    '''
    p = BlogPost.get(key)
    if p is None or not p.static:
        return None
    if publish_only and p.state!=POST_PUBLISHED:
        return None
    return p

def list_tags():
    return BlogTag.all().filter('tag_count >', 0).order('tag_name').fetch(1000)

def create_post():
    pass

def get_pages():
    return BlogPost.all().filter('post_static =', True).order('-post_date').fetch(1000)

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
