# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import random
from urllib.parse import quote

from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy import signals

from nice.config import AGENT
from nice.utils.BloomFilter import BloomFilter


class TutorialSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        n = random.randint(0, len(AGENT) - 1)
        ua = AGENT[n]
        # request.headers.setdefault('User-Agent', ua)
        request.headers.setdefault('User-Agent',
                                   # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
                                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                                   )


class FilterMiddleware(object):
    def __init__(self):
        self.filter = BloomFilter(key='dalaose')

    def process_request(self, request, spider):
        if request.url not in spider.start_urls and len(spider.start_urls) > 0:
            if request.method == 'GET' and self.filter.is_contains(quote(request.url)):
                raise IgnoreRequest("IgnoreRequest : %s" % request.url)
            else:
                fingerprint = quote(request.url) + request.body.decode('utf8')
                if self.filter.is_contains(fingerprint):
                    raise IgnoreRequest("IgnoreRequest : %s" % request.url)
