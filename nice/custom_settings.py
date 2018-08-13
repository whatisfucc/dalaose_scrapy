#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: fzk
# @Time  13:31

SPLASH_URL = 'http://132.232.33.220:8050'

DOWNLOADER_MIDDLEWARES = {'scrapy_splash.SplashCookiesMiddleware': 723,
                          'scrapy_splash.SplashMiddleware': 725,
                          'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
                          'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                          'nice.middlewares.RotateUserAgentMiddleware': 543,
                          'nice.middlewares.FilterMiddleware': 1,
                          }

SPIDER_MIDDLEWARES = {'scrapy_splash.SplashDeduplicateArgsMiddleware': 100}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
