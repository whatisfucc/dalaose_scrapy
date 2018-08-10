# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.parse import urlparse
from os.path import basename, dirname, join

from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request


class NicePipeline(object):
    def process_item(self, item, spider):
        return item


class NiceImgDownloadPipeline(ImagesPipeline):
    default_headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        if item['file_type'] == 'photo':
            image_url = item['source']
            print('source', item['source'])
            self.default_headers['referer'] = image_url
            yield Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class NiceTextPipeline(object):
    def process_item(self, item, spider):
        if item['file_type'] == 'text':
            if not os.path.exists('txt' + os.sep + item['menu']):
                os.mkdir('txt' + os.sep + item['menu'])
            with open(os.sep.join(('txt', item['menu'], item['title'] + '.txt')), 'w') as f:
                f.write(item['text'])


class NiceFilmPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for url in item['film_urls']:
            yield Request(url, meta={'file_name': join(item['menu'], item['title'])})

    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        file_name = request.meta['file_name']
        return join(file_name, basename(path))
