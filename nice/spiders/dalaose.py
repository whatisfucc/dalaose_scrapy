#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: fzk
# @Time  11:44

import re
from urllib.parse import urljoin

import scrapy
import m3u8

from nice.items import NiceItemPhoto


class DalaoseSpider(scrapy.Spider):
    start_urls = [
        'http://www.dalaovod111.com'
    ]
    name = 'dalaose_spider'

    def parse(self, response):
        item = NiceItemPhoto()
        menu = {'网站视频': '1',
                '网站图片': '2',
                '网站小说': '3'}
        uls = response.xpath('//ul[@class="nav_menu clearfix"]')
        for ul in uls:
            menu_type = ul.xpath('li/a/text()').extract_first()
            for li in ul.xpath('li'):
                menu_href = li.xpath('a/@href').extract_first()
                # 这里做了过滤，只爬视频
                if menu_href != '#' and menu_type == '网站视频':
                    yield scrapy.Request(urljoin(response.url, menu_href), callback=self.parse_menu,
                                         meta={'item': item, 'menu_type': menu.get(menu_type)})

    def parse_menu(self, response):
        menu_type = response.meta['menu_type']
        detail_type = {'1': self.parse_movies_detail, '2': self.parse_photo_detail, '3': self.parse_text_detail}
        item = response.meta['item']
        if menu_type == '1':
            for li in response.xpath('//ul[@class="poster"]/li'):
                if li.xpath('a/@href'):
                    yield scrapy.Request(urljoin(response.url, li.xpath('a/@href').extract_first()),
                                         callback=detail_type.get(menu_type), meta={'item': item})
        else:
            for li in response.xpath('//div[@class="text flare"]/ul/li'):
                if li.xpath('a/@href'):
                    yield scrapy.Request(urljoin(response.url, li.xpath('a/@href').extract_first()),
                                         callback=detail_type.get(menu_type), meta={'item': item})

        for a in response.xpath('//div[@class="pagination"]/a'):
            if a.xpath('text()').extract_first() == '下一页':
                yield scrapy.Request(urljoin(response.url, a.xpath('@href').extract_first()),
                                     callback=self.parse_menu,
                                     meta={'item': item, 'menu_type': response.meta['menu_type']})

    def parse_photo_detail(self, response):
        pass
        # print('in parse_photo_detail')
        # item = response.meta['item']
        # item['file_type'] = 'photo'
        # for image in response.xpath('//div[@class="wcen"]/img'):
        #     item['source'] = image.xpath('@src').extract_first()
        #     yield item

    def parse_text_detail(self, response):
        text = response.xpath('//div[@class="main_box py20"]/text()').extract()
        item = response.meta['item']
        item['menu'] = response.xpath('//span[@class="position_left"]/a[2]/text()').extract_first()
        item['title'] = response.xpath('//div[@class="w980 py20"]/h1/text()').extract_first()
        item['source'] = response.url
        item['file_type'] = 'text'
        item['text'] = '\n'.join(text)
        yield item

    def parse_movies_detail(self, response):
        item = NiceItemPhoto()
        flag = re.search('video src="(.*?)"', response.text)
        if flag:
            m3u8_uri = flag.group(1)
            item['menu'] = response.xpath('//span[@class="position_left"]/a[2]/text()').extract_first()
            item['title'] = response.xpath('//div[@class="w980 py20"]/h1/text()').extract_first()
            item['source'] = response.url
            # item['m3u8_uri'] = m3u8_uri
            yield scrapy.Request(m3u8_uri, callback=self.get_m3u8_uri, meta={'m3u8_uri': m3u8_uri, 'item': item})

    def get_m3u8_uri(self, response):
        item = response.meta['item']
        m3u8_uri = response.meta['m3u8_uri']
        m3u8_obj = m3u8.loads(response.text)
        item['film_urls'] = list(map(lambda x: urljoin(m3u8_uri, x), m3u8_obj.files)) + [m3u8_uri]
        item['file_type'] = 'film'
        yield item

