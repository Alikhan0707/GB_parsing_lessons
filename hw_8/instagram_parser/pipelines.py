# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import scrapy
import os
from urllib.parse import urlparse


class InstagramParserPipeline:

    def __init__(self):
        client = MongoClient('192.168.8.105', 27017)
        self.mongo_database = client.users_data

    def process_item(self, item, spider):
        collection = self.mongo_database[spider.name]
        collection.update_one(item, {'$set': item}, upsert=True)
        return item


class InstagramImagesPipline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['profile_image']:
            try:
                yield scrapy.Request(item['profile_image'], meta=item)
            except Exception as e:
                print(e)

    def file_path(self, request, response=None, info=None):
        item = request.meta
        name = item['username']
        return f'{name}/' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results:
            item['profile_image'] = [i[1] for i in results if i[0]]

        return item
