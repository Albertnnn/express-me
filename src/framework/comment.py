#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Simple API for comment.
'''

from google.appengine.ext import db as db

from framework import store
from framework import validator

def create(ref, email, name, content, ip, approval=True, pending_time=None):
    '''
    Create a comment by given ref, email, name, content, ip, approval and pending_time.
    '''
    validator.check_str(ref, 'ref', False)
    validator.check_email(email, 'email')
    validator.check_str(name, 'name', False)
    validator.check_text(content, False)
    if approval:
        pending_time = None
    c = Comment(ref=ref, email=email, name=name, content=content, ip=ip, approval=approval, pending_time=pending_time)
    c.put()
    return c

def approve(key):
    '''
    Approve a comment.
    '''
    c = Comment.get(key)
    if (c is not None) and (not c.approval):
        c.approval = True
        c.put()

def reject(key):
    '''
    Reject a comment. Reject a comment does make it hidden but not delete it.
    '''
    c = Comment.get(key)
    if (c is not None) and c.approval:
        c.approval = False
        c.pending_time = None
        c.put()

def delete(key):
    '''
    Delete a comment by given key.
    '''
    c = Comment.get(key)
    if c is not None:
        c.delete()

def delete_all(ref_key):
    '''
    Delete all comments associated with the reference key. 
    This does not delete all comments immediately from data store. 
    Instead, it add a record in PendingDeleteComment and wait 
    cron job to delete them.
    '''
    p = PendingDeleteComment(ref=ref_key)
    p.put()

def cron_delete_all(ref_key):
    '''
    Delete all comments associated with the reference key. 
    ONLY called by cron job!!!
    '''
    cs = Comment.all().filter('ref =', ref_key).fetch(1000)
    for c in cs:
        c.delete()

class PendingDeleteComment(store.BaseModel):
    '''
    Store reference key that need to remove comments associated with it.
    '''
    ref = db.StringProperty(required=True)

class Comment(store.BaseModel):
    '''
    Store a single comment
    '''
    ref = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    ip = db.StringProperty()
    approval = db.BooleanProperty(required=True, default=True)
    pending_time = db.DateTimeProperty()
