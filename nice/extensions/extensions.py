#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Tiem  2017/11/23

import os

from scrapy import signals


class Extensions(object):
    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        method = cls()
        crawler.signals.connect(method.scrapy_started, signal=signals.engine_started)
        crawler.signals.connect(method.scrapy_stopped, signal=signals.engine_stopped)
        crawler.signals.connect(method.spider_started, signal=signals.spider_opened)
        crawler.signals.connect(method.spider_stopped, signal=signals.spider_closed)
        crawler.signals.connect(method.spider_errored, signal=signals.spider_error)
        return method

    def scrapy_started(self):
        print('scrapy starting.....')

    def scrapy_stopped(self):
        print('scrapy stopping.....')

    def spider_started(self, spider):
        from nice.settings import ABSOLUTE_PATH
        os.listdir(ABSOLUTE_PATH)
        print(spider.name + ': started....')
        print(os.listdir(ABSOLUTE_PATH))

    def spider_stopped(self, spider):
        from scrapy.cmdline import execute
        from nice.settings import ABSOLUTE_PATH
        print(os.listdir(ABSOLUTE_PATH))

        print(spider.name + ': stopped....')

    def spider_errored(self, failure, response, spider):
        import traceback
        traceback.print_exc()
        # client.captureException(tags={'spider': spider.name})
