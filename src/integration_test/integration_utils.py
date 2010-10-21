#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Utils for integration test.
'''

import os
import random

def dummy_title(word_list, word_count):
    '''
    Generate dummy title.
    '''
    L = []
    MAX = len(word_list) - 1
    r = int(word_count * 0.2)
    words = word_count + random.randint(-r, r)
    if words<=0:
        words = 1
    for i in range(words):
        n = random.randint(0, MAX)
        L.append(word_list[n])
    return ' '.join(L)

def dummy_paragraph(word_list, paragraph_count, word_count):
    '''
    Generate dummy paragraph.
    '''
    L = []
    MAX = len(word_list) - 1
    for i in range(paragraph_count):
        P = []
        r = int(word_count * 0.2)
        words = word_count + random.randint(-r, r)
        if words<=0:
            words = 1
        for j in range(words):
            n = random.randint(0, MAX)
            P.append(word_list[n])
        L.append('<p>' + ' '.join(P) + '</p>')
    return '\n'.join(L)

def _load_words():
    root_path = os.path.split(__file__)[0]
    file = open(os.path.join(root_path, 'words.txt'), 'r')
    words = []
    for line in file:
        s = line.strip()
        if s:
            words.append(s)
    file.close()
    return words
