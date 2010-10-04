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
POST_DELETED = 3

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
    author = db.StringProperty() # user's name
    state = db.IntegerProperty(required=True, default=POST_PUBLISHED)
    title = db.StringProperty(required=True)
    excerpt = db.TextProperty(required=True)
    content = db.TextProperty(required=True)
    category = db.ReferenceProperty(required=True, reference_class=BlogCategory)
    tags = db.StringListProperty()
    static = db.BooleanProperty(default=False)
    allow_comment = db.BooleanProperty(required=True, default=True)

    def tags_as_string(self):
        return ','.join(self.tags)

    def url(self):
        return '%s/%s' % (self.static and 'page' or 'post', self.id)

def create_post(user, state, title, content, category, tags_str='', allow_comment=True):
    '''
    Create a post by given user, state, title, etc.
    
    Args:
        user: User object.
        state: Post state.
        title: Post title.
        content: Post content.
        category: Post category.
        tags_str: Post tags as a string, default to ''.
        allow_comment: True if allow comment, default to True.
    
    Returns:
        The created BlogPost object.
    '''
    tags = [t.strip() for t in tags_str.split(',')]
    tags = [t for t in tags if t]
    # TODO: fix me...
    excerpt = content
    p = BlogPost(
            ref = user.id,
            author = user.nicename,
            state = state,
            title = title,
            excerpt = excerpt,
            content = content,
            category = category,
            tags = tags,
            static = False,
            allow_comment = allow_comment
    )
    p.put()
    return p

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
    if cursor:
        q.with_cursor(cursor)
    result = q.fetch(limit)
    cursor = q.cursor()
    if not store.has_more(q, cursor):
        cursor = None
    return result, cursor

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

def get_posts(limit=50, cursor=None, ref_user=None, category=None, published_only=True):
    '''
    get posts by user's key, category, published state, etc.
    
    Returns:
        A tuple (Posts as list, cursor for next query).
    '''
    if published_only:
        return _query_posts(limit, cursor, ref_user=ref_user, static=False, category=category, state=POST_PUBLISHED)
    else:
        return _query_posts(limit, cursor, ref_user=ref_user, static=False, category=category)

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
    cat = BlogCategory(name=name, description=description, count=0)
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
    categories = BlogCategory.all().order('name').fetch(100)
    if not categories:
        categories.append(create_category('Uncategorized'))
    return categories

def undelete_post(key):
    '''
    Undelete a post.
    
    Args:
        key: key of post.
    Returns:
        True if operation successfully, otherwise False.
    '''
    post = get_post(key, published_only=False)
    if post and post.state==POST_DELETED:
        post.state = POST_DRAFT
        post.put()
        return True
    return False

def pending_post(key):
    '''
    Pending a post and wait for approval.
    
    Args:
        key: key of post.
    Returns:
        True if operation successfully, otherwise False.
    '''
    post = get_post(key, published_only=False)
    if post and post.state==POST_DRAFT:
        post.state = POST_PENDING
        post.put()
        return True
    return False

def publish_post(key):
    '''
    Publish a post.
    
    Args:
        key: key of post.
    Returns:
        True if operation successfully, otherwise False.
    '''
    post = get_post(key, published_only=False)
    if post and post.state==POST_DRAFT:
        post.state = POST_PUBLISHED
        post.put()
        return True
    return False

def unpublish_post(key):
    '''
    Unpublish a post.
    
    Args:
        key: key of post.
    Returns:
        True if operation successfully, otherwise False.
    '''
    post = get_post(key, published_only=True)
    if post:
        post.state = POST_DRAFT
        post.put()
        return True
    return False

def approve_post(key):
    '''
    Approve a pending post.
    Args:
        key: key of post.
    Returns:
        True if operation successfully, otherwise False.
    '''
    post = get_post(key, published_only=False)
    if post and post.state==POST_PENDING:
        post.state = POST_PUBLISHED
        post.put()
        return True
    return False
    
def delete_post(key, permanent=False):
    '''
    Delete a post.
    
    Args:
        key: key of post.
        permanent: True if delete permanently, default to False.
    Returns:
        True if operation successfully, otherwise False.
    '''
    post = get_post(key, published_only=False)
    if post:
        if not permanent and post.state!=POST_DELETED:
            post.state = POST_DELETED
            post.put()
            return True
        # only DELETED post can be deleted permanently:
        elif permanent and post.state==POST_DELETED:
            post.delete()
            return True
    return False

def get_post(key, static=False, published_only=True):
    '''
    get BlogPost by key.
    
    Args:
        key: key of post.
        published_only: if post is published.
    Return: BlogPost object, or None if no such post.
    '''
    p = BlogPost.get(key)
    if p is None:
        return None
    if p.static!=static:
        return None
    if published_only and p.state!=POST_PUBLISHED:
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
