#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Simple functions to send mail.
'''

from google.appengine.api import mail

def send(sender_address, to_address, subject, body, html=None):
    '''
    Send mail.
    
    Args:
        sender_address: sender's address
        to_address: receiver's address
        subject: subject of the mail
        body: body of the mail
        html: HTML body of the mail, default to None
    '''
    kw = {}
    if html:
        kw['html'] = html
    mail.send_mail(sender_address, to_address, subject, body, **kw)
