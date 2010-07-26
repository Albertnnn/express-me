#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Blog app management.
'''

from blog import store

from exweb import context

from manage import shared

import manage

appmenus = [
        ('Post', [
                shared.AppMenuItem(shared.USER_ROLE_CONTRIBUTOR, 'Edit', 'edit_post'),
                shared.AppMenuItem(shared.USER_ROLE_CONTRIBUTOR, 'Add New', 'add_post'),
                shared.AppMenuItem(shared.USER_ROLE_CONTRIBUTOR, 'Tags', 'tags'),
                shared.AppMenuItem(shared.USER_ROLE_ADMINISTRATOR, 'Categories', 'categories'),
                shared.AppMenuItem(shared.USER_ROLE_CONTRIBUTOR, 'Settings', 'settings')
        ]),
        ('Page', [
                shared.AppMenuItem(shared.USER_ROLE_ADMINISTRATOR, 'Edit', 'edit_page'),
                shared.AppMenuItem(shared.USER_ROLE_ADMINISTRATOR, 'Add New', 'add_page')
        ])
]

def manage_nav():
    '''
    Get app's navigation settings so user can customize their navigation bar.
    
    Returns:
        A list contains (title, url).
    '''
    navs = [('Posts', '/blog/')]
    pages = store.get_pages()
    for page in pages:
        navs.append((page.post_title, '/blog/page/' + str(page.key())))
    return navs

def manage_app(user, action, **args):
    f = ''.join(['__handle_', context.method, '_', action, '()'])
    # we are going to call function by name '__handle_' + (get or post) + _ + action
    return eval(f)

def __handle_get_add_page():
    '''
    show form of creating a new page
    '''
    return {
            'template' : 'editor.html',
            'post_action_title' : 'Add a New Page',
            'post_title' : '',
            'post_content' : ''
    }

def __handle_get_add_post():
    '''
    show form of creating a new post
    '''
    cats = store.get_categories()
    return {
            'template' : 'editor.html',
            'post_action_title' : 'Add a New Post',
            'post_title' : '',
            'post_category' : cats[0],
            'post_content' : '',
            'post_tags' : '',
            'tags' : store.get_hot_tags(10),
            'categories' : cats
    }

def __handle_post_add_page():
    '''
    create a new page
    '''
    form = context.form
    title = form.get_escape('title')
    content = form.get('content')
    post = store.BlogPost(
            post_static = True,
            post_owner = context.user,
            post_title = title,
            post_content = content,
            post_excerpt = '',
            post_category = None,
            post_tags = [],
            post_state = store.POST_STATE_PUBLISHED
    )
    post.put()
    return {
            'template' : 'message.html',
            'message' : 'Page published.',
            'detail' : 'Your page has been published successfully!',
            'url' : '/blog/page/' + str(post.key()),
            'url_title' : 'View Page',
            'url_blank' : True
    }

def __handle_post_add_post():
    '''
    create a new post
    '''
    form = context.form
    title = form.get_escape('title')
    content = form.get('content')
    categoryKey = form.get('categoryKey')
    tags = __get_tags(form)
    state = store.POST_STATE_PUBLISHED
    if context.user.user_role >= shared.USER_ROLE_CONTRIBUTOR:
        state = store.POST_STATE_PENDING
    # create a new post:
    post = store.BlogPost(
            post_static = False,
            post_owner = context.user,
            post_title = title,
            post_content = content,
            post_excerpt = '',
            post_category = store.get_category(categoryKey),
            post_tags = [t.lower() for t in tags],
            post_state = state
    )
    post.put()
    for t in tags:
        store.create_tag(t, 1)
    dict = {
            'template' : 'message.html',
            'message' : state==store.POST_STATE_PUBLISHED and 'Post published.' or 'Post submitted.',
            'detail' : state==store.POST_STATE_PUBLISHED and 'Your post has been published successfully!' or 'Your post has been submitted and pending for approval.',
    }
    if state==store.POST_STATE_PUBLISHED:
        dict['url'] = '/blog/post/' + str(post.key())
        dict['url_title'] = 'View Post'
        dict['url_blank'] = True
    return dict

def __handle_get_edit_page():
    id = context.form.get('id', '')
    if id:
        post = store.BlogPost.get(id)
        return {
                'template' : 'editor.html',
                'post_action_title' : 'Edit a Page',
                'id' : id,
                'post_title' : post.post_title,
                'post_content' : post.post_content
        }
    return {
            'template' : 'page_edit_list.html',
            'posts' : store.get_pages()
    }

def __handle_get_edit_post():
    id = context.form.get('id', '')
    if id:
        post = store.BlogPost.get(id)
        return {
                'template' : 'editor.html',
                'post_action_title' : 'Edit a Post',
                'id' : id,
                'post_title' : post.post_title,
                'post_category' : post.post_category,
                'post_content' : post.post_content,
                'post_tags' : post.post_tags_as_string(),
                'tags' : store.get_hot_tags(10),
                'categories' : store.get_categories()
        }
    from time import time
    posts = store.get_posts(time(), 21)
    return {
            'template' : 'post_edit_list.html',
            'categories' : store.get_categories(),
            'posts' : posts
    }

def __handle_post_edit_page():
    form = context.form
    id = form.get('id')
    title = form.get_escape('title')
    content = form.get('content')
    post = store.BlogPost.get(id)
    post.post_title = title
    post.post_content = content
    post.put()
    return {
            'template' : 'message.html',
            'message' : 'Page published.',
            'detail' : 'Your page has been published successfully!',
            'url' : '/blog/page/' + id,
            'url_title' : 'View Page',
            'url_blank' : True
    }

def __handle_post_edit_post():
    form = context.form
    id = form.get('id')
    title = form.get_escape('title')
    content = form.get('content')
    categoryKey = form.get('categoryKey')
    tags = __get_tags(form)
    post = store.BlogPost.get(id)
    post.post_title = title
    post.post_content = content
    post.post_category = store.get_category(categoryKey)
    # handle tags:
    old_tags = post.post_tags[:]
    post.post_tags = [t.lower() for t in tags]
    new_tags = post.post_tags[:]
    post.put()
    for t in new_tags:
        if t in old_tags:
            old_tags.remove(t)
        else:
            store.create_tag(t, 1)
    for t in old_tags:
        store.create_tag(t, -1)
    dict = {
            'template' : 'message.html',
            'message' : post.post_state==store.POST_STATE_PUBLISHED and 'Post published.' or 'Post submitted.',
            'detail' : post.post_state==store.POST_STATE_PUBLISHED and 'Your post has been published successfully!' or 'Your post has been submitted and pending for approval.'
    }
    if post.post_state==store.POST_STATE_PUBLISHED:
        dict['url'] = '/blog/post/' + id
        dict['url_title'] = 'View Post'
        dict['url_blank'] = True
    return dict

def __handle_get_categories():
    return {
            'template' : 'post_categories.html',
            'categories' : store.get_categories()
    }

def __handle_post_categories():
    form = context.form
    name = form.get_escape('name')
    description = form.get_escape('description')
    store.create_category(name, description)
    return {
            'template' : 'message.html',
            'message' : 'Category created.',
            'detail' : 'Your category has been created successfully!',
            'url' : '?app=blog&action=post_categories',
            'url_title' : 'Continue'
    }

def __handle_get_settings():
    settings = shared.get_settings('blog_setting')
    return {
            'template' : 'setting.html',
            'posts_per_page' : shared.get_setting(settings, 'posts_per_page', '20'),
            'posts_in_feed' : shared.get_setting(settings, 'posts_in_feed', '20'),
            'feed_full' : shared.get_setting(settings, 'feed_full', 'True'),
            'feed_title' : shared.get_setting(settings, 'feed_title', 'Rss Feed'),
            'feed_desc' : shared.get_setting(settings, 'feed_desc', 'Subscribe Rss Feed'),
            'feed_proxy' : shared.get_setting(settings, 'feed_proxy', ''),
            'comment_allow' : shared.get_setting(settings, 'comment_allow', 'registered')
    }

def __handle_post_settings():
    '''
    Save all settings
    '''
    form = context.form
    for key in ['posts_per_page', 'posts_in_feed', 'feed_full', 'feed_title', 'feed_desc', 'feed_proxy', 'comment_allow']:
        shared.save_setting('blog_setting', key, form.get(key))
    dict = __handle_get_settings()
    dict['message'] = 'Your settings are saved.'
    return dict

def __handle_get_tags():
    return {
            'template' : 'post_tags.html',
            'tags' : store.get_tags(),
            'hot_tags' : store.get_hot_tags(20)
    }

def __get_tags(form):
    tags = form.get_escape('tags').split(',')
    return [t.strip() for t in tags if t.strip()]
