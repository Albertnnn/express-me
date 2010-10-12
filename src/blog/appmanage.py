#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Blog app management.
'''

import logging

from framework import ApplicationError
from framework import store
from framework.encode import encode_html

from blog import model

from manage import AppMenu
from manage import AppMenuItem

def get_menus():
    '''
    Get menus for management.
    '''
    post = AppMenu('Post',
            AppMenuItem(store.ROLE_CONTRIBUTOR, 'Edit', 'edit_post'),
            AppMenuItem(store.ROLE_CONTRIBUTOR, 'Add New', 'add_post'),
            AppMenuItem(store.ROLE_EDITOR, 'Categories', 'categories'),
            AppMenuItem(store.ROLE_CONTRIBUTOR, 'Tags', 'tags'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Options', 'options')
    )
    page = AppMenu('Page',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Edit', 'edit_page'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Add New', 'add_page')
    )
    return (post, page,)

def get_navigation():
    '''
    Get navigation menu.
    '''
    L = [('blog', '/',)]
    pages = model.get_pages(True)
    for page in pages:
        L.append((page.title, '/page/%s' % page.id,))
    return L

def __get_page_list(context):
    ps = model.get_pages(published_only=False)
    return {
            '__view__' : 'manage_page_list',
            'ps' : ps,
    }

def __get_post_list(user, context):
    category = None
    cat = context.get_argument('category', '')
    if cat:
        category = model.get_category(cat)
    offset = context.get_argument('offset', '')
    if not offset:
        offset = None
    index = 1
    if offset:
        index = int(context.get_argument('index'))
    categories = model.get_categories()
    ref = None
    if user.role >= store.ROLE_AUTHOR:
        ref = user.id
    ps, next_cursor = model.get_posts(5, offset, ref, category, published_only=False)
    return {
            '__view__' : 'manage_post_list',
            'static' : False,
            'ps' : ps,
            'category' : cat,
            'categories' : categories,
            'offset' : offset,
            'next' : next_cursor,
            'index' : index,
    }

def _edit_post(user, app, context):
    if context.method=='get':
        btn = context.get_argument('btn', '')
        if btn=='edit':
            p =  model.get_post(context.get_argument('id'), published_only=False)
            if user.role >= store.ROLE_AUTHOR and p.ref != user.id:
                raise ApplicationError('Permission denied.')
            return {
                    '__view__' : 'manage_editor',
                    'post' : p,
                    'categories' : model.get_categories(),
            }
        return __get_post_list(user, context)

    if context.method=='post':
        btn = context.get_argument('btn', '')
        id = context.get_argument('id', '')
        ok = False
        if btn=='edit' and user.role >= store.ROLE_AUTHOR:
            p = model.get_post(id, False, False)
            if p and p.ref==user.id:
                title = context.get_argument('title')
                content = context.get_argument('content')
                category = model.get_category(context.get_argument('category'))
                tags = context.get_argument('tags')
                draft = context.get_argument('draft')=='True'
                allow_comment = context.get_argument('allow_comment')=='True'
                state = model.POST_PUBLISHED
                if draft:
                    state = model.POST_DRAFT
                p = model.update_post(id, user, state, title, content, category, tags, allow_comment)
                return __json_result(False, p)
        elif btn=='publish' and user.role >= store.ROLE_AUTHOR:
            p = model.get_post(id, False, False)
            if p and p.ref==user.id:
                ok = model.pending_post(id)
        elif btn=='publish' and user.role <= store.ROLE_EDITOR:
            ok = model.publish_post(id)
        elif btn=='unpublish' and user.role <= store.ROLE_EDITOR:
            ok = model.unpublish_post(id)
        elif btn=='approve' and user.role <= store.ROLE_EDITOR:
            ok = model.approve_post(id)
        elif btn=='delete' and user.role <= store.ROLE_EDITOR:
            ok = model.delete_post(id)
        elif btn=='perm_delete' and user.role <= store.ROLE_EDITOR:
            ok = model.delete_post(id, permanent=True)
        elif btn=='undelete' and user.role <= store.ROLE_EDITOR:
            ok = model.undelete_post(id)
        if not ok:
            logging.warning('Operation failed: %s, id=%s' % (btn, id,))
        return __get_post_list(user, context)

def _edit_page(user, app, context):
    if context.method=='get':
        btn = context.get_argument('btn', '')
        if btn=='edit':
            p =  model.get_post(context.get_argument('id'), static=True, published_only=False)
            return {
                    '__view__' : 'manage_editor',
                    'post' : p,
            }
        return __get_page_list(context)

    if context.method=='post':
        btn = context.get_argument('btn', '')
        id = context.get_argument('id', '')
        ok = False
        if btn=='edit':
            p = model.get_post(id, True, False)
            if p:
                title = context.get_argument('title')
                content = context.get_argument('content')
                draft = context.get_argument('draft')=='True'
                allow_comment = context.get_argument('allow_comment')=='True'
                state = model.POST_PUBLISHED
                if draft:
                    state = model.POST_DRAFT
                p = model.update_page(id, user, state, title, content, allow_comment)
                return __json_result(False, p)
        elif btn=='publish':
            ok = model.publish_post(id, static=True)
        elif btn=='unpublish':
            ok = model.unpublish_post(id, static=True)
        elif btn=='delete':
            ok = model.delete_post(id, static=True)
        elif btn=='perm_delete':
            ok = model.delete_post(id, static=True, permanent=True)
        elif btn=='undelete':
            ok = model.undelete_post(id, static=True)
        if not ok:
            logging.warning('Operation failed: %s, id=%s' % (btn, id,))
        return __get_page_list(context)

def __json_result(add, post):
    return r'json:{"add":%s,"id":"%s","static":%s,"title":"%s","state":%s,"url":"/blog/%s"}' \
            % ( add and 'true' or 'false', \
                post.id, \
                post.static and 'true' or 'false', \
                encode_html(post.title), \
                post.state, \
                post.url() \
            )

def __empty_post(user, static):
    return {
            'id' : '',
            'static' : static,
            'title' : '',
            'content' : '',
            'ref' : user.id,
            'category' : {'id':''},
            'author' : user.nicename,
            'tags_as_string' : lambda : '',
            'state' : 0,
            'allow_comment' : True,
    }

def _add_post(user, app, context):
    if context.method=='get':
        return {
                '__view__' : 'manage_editor',
                'post' : __empty_post(user, False),
                'categories' : model.get_categories(),
        }
    if context.method=='post':
        title = context.get_argument('title')
        content = context.get_argument('content')
        category = context.get_argument('category')
        tags = context.get_argument('tags')
        draft = context.get_argument('draft')=='True'
        allow_comment = context.get_argument('allow_comment')=='True'
        state = model.POST_PUBLISHED
        if draft:
            state = model.POST_DRAFT
        p = model.create_post(user, state, title, content, model.get_category(category), tags, allow_comment)
        return __json_result(True, p)

def _add_page(user, app, context):
    if context.method=='get':
        return {
                '__view__' : 'manage_editor',
                'post' : __empty_post(user, True),
        }
    if context.method=='post':
        title = context.get_argument('title')
        content = context.get_argument('content')
        draft = context.get_argument('draft')=='True'
        allow_comment = context.get_argument('allow_comment')=='True'
        state = model.POST_PUBLISHED
        if draft:
            state = model.POST_DRAFT
        elif user.role>=store.ROLE_AUTHOR:
            state = model.POST_PENDING
        p = model.create_page(user, state, title, content, allow_comment)
        return r'json:{"add":true,"id":"%s","static":%s,"title":"%s","state":%s,"url":"/blog/%s"}' \
                % (p.id, p.static and 'true' or 'false', encode_html(p.title), state, p.url())

def __get_category_list(info=None):
    m = {
            '__view__' : 'manage_category_list',
            'categories' : model.get_categories(),
    }
    if info:
        m['info'] = info
    return m

def _categories(user, app, context):
    btn = context.get_argument('btn', '')
    if btn=='add':
        # add category:
        if context.method=='get':
            return {
                    '__view__' : 'manage_category_editor',
                    'add' : True,
                    'category' : model.BlogCategory(name='Unamed', description=''),
            }
        else:
            name = context.get_argument('name')
            description = context.get_argument('description', '')
            model.create_category(name, description)
            return __get_category_list('Category "%s" created.' % name)
    if btn=='edit':
        id = context.get_argument('id')
        category = model.get_category(id)
        if context.method=='get':
            return {
                    '__view__' : 'manage_category_editor',
                    'add' : False,
                    'category' : category,
            }
        else:
            name = context.get_argument('name')
            description = context.get_argument('description', '')
            category.name = name
            category.description = description
            category.put()
            return __get_category_list('Category "%s" updated.' % name)
    return __get_category_list()

POST_OPTIONS = 'blog.post.options'

def _options(user, app, context):
    info = ''
    if context.method=='post':
        show_abstract = context.get_argument('show_abstract')
        feed_proxy = context.get_argument('feed_proxy')
        store.set_setting('show_abstract', show_abstract, POST_OPTIONS)
        store.set_setting('feed_proxy', feed_proxy, POST_OPTIONS)
        info = 'Your options are saved.'
    # load options:
    options = store.get_settings(POST_OPTIONS)
    for k, v in (('show_abstract', 'False'), ('feed_proxy', '')):
        if not k in options:
            options[k] = v
    return {
            '__view__' : 'manage_option',
            'options' : options,
            'info' : info,
    }

def manage(user, app, command, context):
    map = {
           'edit_post' : _edit_post,
           'add_post' : _add_post,
           'edit_page' : _edit_page,
           'add_page' : _add_page,
           'categories' : _categories,
           'options' : _options,
    }
    return map[command](user, app, context)
