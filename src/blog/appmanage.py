#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Blog app management.
'''

from framework import store

from blog import model

from manage.common import AppMenu
from manage.common import AppMenuItem

def get_menus():
    '''
    Get menus for management.
    '''
    post = AppMenu('Post',
            AppMenuItem(store.ROLE_CONTRIBUTOR, 'Edit', 'edit_post'),
            AppMenuItem(store.ROLE_CONTRIBUTOR, 'Add New', 'add_post'),
            AppMenuItem(store.ROLE_CONTRIBUTOR, 'Tags', 'tags')
    )
    page = AppMenu('Page',
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Edit', 'edit_page'),
            AppMenuItem(store.ROLE_ADMINISTRATOR, 'Add New', 'add_page')
    )
    return (post, page,)

def _edit_post(user, app, context):
    pass

def _empty_post(user, static):
    return {
            'id' : '',
            'static' : static,
            'title' : '',
            'content' : '',
            'ref' : user.id,
            'author' : user.nicename,
            'tags_as_string' : lambda : '',
    }

def _add_post(user, app, context):
    if context.method=='get':
        return {
                '__view__' : 'manage_editor',
                'post' : _empty_post(user, False),
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
        elif user.role>=store.ROLE_AUTHOR:
            state = model.POST_PENDING
        post = model.create_post(user, state, title, content, model.get_category(category), tags, allow_comment)
        msg_title, msg = {
                model.POST_PUBLISHED : ('Post published', r'Your post "%s" has been published.' % title,),
                model.POST_DRAFT : ('Post saved as draft', r'Your post "%s" has been saved as draft.' % title,),
                model.POST_PENDING : ('Post saved and pending for approval', r'Your post "%s" has been saved and pending for approval.' % title,),
        }[state]
        buttons = [('View Post', '/blog/post/%s' % post.id, True)]
        if state==model.POST_DRAFT or state==model.POST_PENDING:
            buttons = [('Edit Post', '/manage/?app=blog&command=edit_post&id=%s' % post.id, False)]
        buttons.append(('Add Another', '/manage/?app=blog&command=add_post', False))
        return {
                '__view__' : 'manage_message',
                'title' : msg_title,
                'message' : msg,
                'buttons' : buttons,
        }

def _add_page(user, app, context):
    if context.method=='get':
        return {
                '__view__' : 'manage_editor',
                'post' : _empty_post(user, True),
        }

def manage(user, app, command, context):
    map = {
           'edit_post' : _edit_post,
           'add_post' : _add_post,
           'add_page' : _add_page,
    }
    return map[command](user, app, context)
