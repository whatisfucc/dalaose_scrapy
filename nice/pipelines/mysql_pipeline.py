#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time  15:25

import arrow

from nice.settings import INSERT_NUM

from nice.config import TABLE, DB_CONNECT_STRING


class MysqlPipeline(object):
    def __init__(self):
        self.table = ''
        self.wanted_items_insert = []
        self.wanted_insert_count = 0

    def process_item(self, item, spider):
        TIME_AREA = 'Asia/Shanghai'
        now_time = arrow.now(TIME_AREA).format('YYYY-MM-DD HH:mm:ss')
        data = item.__dict__['_values']
        self.table = data.pop('table')
        data['spider'] = spider.name
        data['created'] = now_time
        data['modified'] = now_time
        if self.table == TABLE:
            self.wanted_items_insert.append(data)
            self.wanted_insert_count += 1
            if self.wanted_insert_count == INSERT_NUM:
                self.process_items(self.wanted_items_insert, self.table)
                self.wanted_items_insert = []
                self.wanted_insert_count = 0

    def update_item(self, item):
        # 更新操作
        repository = Repository()
        repository.update(item, self.table)

    def process_items(self, items, table):
        try:
            repository = Repository()
            repository.save_datas(items, table)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('存储错误')

    def close_spider(self, spider):
        print('**' * 20)
        print('存储不够1000item的items')
        if self.wanted_items_insert:
            self.process_items(self.wanted_items_insert, table=TABLE)


class Repository(object):
    def __init__(self):
        self.conn = dataset.connect(DB_CONNECT_STRING)

    def save_datas(self, items, table):
        self.conn[table].insert_many(items)

    def update(self, item, table):
        self.conn[table].update(item, keys='no')

