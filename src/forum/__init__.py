#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Forum app that allows users to discuss.
'''

from google.appengine.ext import db
from manage.shared import User

class Forum(db.Model):
    pass

class ForumTopic(db.Model):
    topic_user = db.ReferenceProperty(reference_class=User, required=True)
    topic_forum = db.ReferenceProperty(reference_class=Forum, required=True)
    topic_title = db.StringProperty(required=True)
    topic_content = db.TextProperty(required=True)
    topic_ontop = db.BooleanProperty(default=False)

class ForumReply(db.Model):
    reply_user = db.ReferenceProperty(reference_class=User, required=True)
    reply_topic = db.ReferenceProperty(reference_class=ForumTopic, required=True)
    reply_title = db.StringProperty(required=True)
    reply_content = db.TextProperty(required=True)

class StarredTopic(db.Model):
    pass
