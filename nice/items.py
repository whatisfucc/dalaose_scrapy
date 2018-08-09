# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NiceItemPhoto(scrapy.Item):
    # define the fields for your item here like:
    m3u8_uri = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    menu = scrapy.Field()
    image_paths = scrapy.Field()
    text = scrapy.Field()
    file_type = scrapy.Field()
    film_urls = scrapy.Field()
    file = scrapy.Field()
