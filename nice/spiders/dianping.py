#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: fzk
# @Time  12:01

import re
from urllib.parse import urljoin

from scrapy import Spider, Selector, Request# as SplashRequest
from scrapy_splash import SplashRequest

from nice.items import DianpingItem
from nice.custom_settings import SPLASH_URL, SPIDER_MIDDLEWARES, HTTPCACHE_STORAGE, DOWNLOADER_MIDDLEWARES, \
    DUPEFILTER_CLASS
from nice.utils.dianping_num import get_dianping_num


class DianpingSpider(Spider):
    start_urls = [
        'http://www.dianping.com/beijing/ch10'
    ]
    name = 'dianping_spider'

    custom_settings = {
        'DUPEFILTER_CLASS': DUPEFILTER_CLASS,
        'SPLASH_URL': SPLASH_URL,
        'SPIDER_MIDDLEWARES': SPIDER_MIDDLEWARES,
        'HTTPCACHE_STORAGE': HTTPCACHE_STORAGE,
        'DOWNLOADER_MIDDLEWARES': DOWNLOADER_MIDDLEWARES,
        'ITEM_PIPELINES': {'nice.pipelines.mysql_pipeline.MysqlPipeline': 100}
    }

    download_delay = 0.5

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse)

    def parse(self, response):
        item = DianpingItem()
        uls = response.xpath('//div[@id="metro-nav"]')
        for li in uls.xpath('a'):
            menu_href = li.xpath('@href').extract_first()
            subway_name = li.xpath('string()').extract_first()
            item['subway'] = subway_name
            yield SplashRequest(urljoin(response.url, menu_href), callback=self.parse_menu,
                                meta={'item': item})

    def parse_menu(self, response):
        selector = Selector(response)
        print(response.text)
        item = response.meta['item']
        for li in selector.xpath('//div[@id="shop-all-list"]/ul/li'):
            detail_link = li.xpath('div[@class="pic"]/a/@href').extract_first()
            shop_address = li.xpath(
                'div[@class="txt"]/div[@class="tag-addr"]/span[@class="addr"]/text()').extract_first()
            item['shop_address'] = shop_address
            yield SplashRequest(detail_link, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        selector = Selector(response)
        section = selector.xpath('//div[@class="main"]')
        basic_section = section.xpath('div[@id="basic-info"]')
        shop_name = basic_section.xpath('h1/text()').extract_first()
        level = basic_section.xpath('div[@class="brief-info"]/span/@title').extract_first()
        review_count = basic_section.xpath('string(div[@class="brief-info"]/span[@id="reviewCount"])').extract_first()
        avg_price = self.get_num(basic_section.xpath('span[@id="avgPriceTitle"]'), 'span|text()', 'span')
        score_taste = self.get_num(basic_section.xpath('span[@id="comment_score"]/span[1]'), 'span|text()', 'span')
        score_env = self.get_num(basic_section.xpath('span[@id="comment_score"]/span[2]'), 'span|text()', 'span')
        score_service = self.get_num(basic_section.xpath('span[@id="comment_score"]/span[3]'), 'span|text()', 'span')
        tel = self.get_num(basic_section.xpath('p[@class="expand-info tel"]'), 'span|text()', 'span')
        item['shop_name'] = shop_name
        item['level'] = level
        item['review_count'] = review_count
        item['avg_price'] = avg_price
        item['score_taste'] = score_taste
        item['score_env'] = score_env
        item['score_service'] = score_service
        item['tel'] = tel
        item['source'] = response.url
        item['table'] = 'dianping'
        yield item

    def get_num(self, node, rule_xpath, child_node):
        '''
        :param node 根节点的xpath对象
        :param rule_xpath 相对于根节点的子节点所需xpath规则
        :param child_node 子节点标签
        正则我写死了，无所谓，只针对这一个网站是可行的
        '''
        result = ''
        for num in node.xpath(rule_xpath).extract():
            if child_node in num:
                num = re.search('class="(.*)"', num).group(1)
                result = result + get_dianping_num(num)
            else:
                result = result + num
        return result
