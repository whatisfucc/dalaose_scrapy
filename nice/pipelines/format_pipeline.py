#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: fzk
# @Time  10:58

from nice.utils.hash_md5 import md5


class FilterPipeline(object):
    def process_item(self, item, spider):
        item['no'] = md5(item['source'] + item['menu'] + item['title'])
        return item
