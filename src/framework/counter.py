#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Simple API for counters that support sharding.
'''

import random

from framework import cache
from google.appengine.ext import db

CACHE_KEY_PREFIX = '_sharded_counter_'

def get(name):
    '''
    Retrieve the value for a given sharded counter.
    
    Args:
        name: the name of the counter
    Returns:
        Integer value
    '''
    total = cache.get(CACHE_KEY_PREFIX + name)
    if total is None:
        total = 0
        for counter in ShardedCounter.all().filter('name =', name).fetch(1000):
            total += counter.count
        cache.set(CACHE_KEY_PREFIX + name, str(total))
        return total
    return int(total)

def incr(name, delta=1):
    '''
    Increment the value for a given sharded counter.
    
    Args:
        name: the name of the counter
    '''
    config = ShardedCounterConfig.get_or_insert(name, name=name)
    def tx():
        index = random.randint(0, config.shards-1)
        shard_name = name + str(index)
        counter = ShardedCounter.get_by_key_name(shard_name)
        if counter is None:
            counter = ShardedCounter(key_name=shard_name, name=name)
        counter.count += delta
        counter.put()
    db.run_in_transaction(tx)
    cache.incr(CACHE_KEY_PREFIX + name, delta=delta)

def incr_shards(name, num):
    '''
    Increase the number of shards for a given sharded counter.
    Will never decrease the number of shards.
    
    Args:
        name: the name of the counter
        num: how many shards to use
    '''
    config = ShardedCounterConfig.get_or_insert(name, name=name)
    def tx():
        if config.shards < num:
            config.shards = num
            config.put()
    db.run_in_transaction(tx)

class ShardedCounterConfig(db.Model):
    '''
    Tracks the number of shards for each named counter.
    '''
    name = db.StringProperty(required=True)
    shards = db.IntegerProperty(required=True, default=10)

class ShardedCounter(db.Model):
    '''
    Shards for each named counter
    '''
    name = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True, default=0)
