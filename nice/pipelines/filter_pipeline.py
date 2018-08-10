#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: fzk
# @Time  10:55

from urllib.parse import quote

from nice.utils.BloomFilter import BloomFilter


class FilterPipeline(object):
    def __init__(self):
        self.server = BloomFilter()

    def process_item(self, item, spider):
        item['store'] = True
        if not item.get('http_method'):
            item['http_method'] = 'GET'
        if not item.get('body'):
            item['body'] = ''
        if item['http_method'] == 'GET':
            if self.server.is_contains(item['no']):
                item['store'] = False  # True 为插入，False 为更新
            else:
                self.server.insert(item['no'])  # 当前item的no存进去，为了方便区分队列，这个item是更新还是插入，主要取决于本字段
                self.server.insert(quote(item['source']))
            # item.pop('http_method')
            item.pop('body')
        else:
            fingerprint = quote(item['source']) + item['body']
            if self.server.is_contains(item['no']):
                item['store'] = False
            else:
                self.server.insert(item['no'])
                self.server.insert(fingerprint)
            # item.pop('http_method')
            item.pop('body')
        return item
