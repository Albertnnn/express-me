#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Forum app model.
'''

from google.appengine.ext import db

from framework import store

class Forum(store.BaseModel):
    pass

class ForumTopic(store.BaseModel):
    user = db.StringProperty(required=True)
    forum = db.ReferenceProperty(reference_class=Forum, required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    ontop = db.BooleanProperty(default=False)

class ForumReply(store.BaseModel):
    user = db.StringProperty(required=True)
    topic = db.ReferenceProperty(reference_class=ForumTopic, required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)

class StarredTopic(db.Model):
    pass
