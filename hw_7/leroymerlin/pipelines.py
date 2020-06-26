# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import os
from urllib.parse import urlparse
from pymongo import MongoClient


def price_procesing(list_price: list):

    price_keys = ['price', 'currency', 'measurement']

    if len(list_price) == 3:
        list_price = dict(zip(price_keys, list_price))
    elif len(list_price) == 4:
        price = float('.'.join(map(str, list_price[:2])))
        list_price = list_price[2:]
        list_price.insert(0, price)
        list_price = dict(zip(price_keys, list_price))

    return list_price


class LeroymerlinPipeline(object):

    def __init__(self):
        client = MongoClient('', 27017)
        self.mongo_database = client.products_leroymerlin_db

    def process_item(self, item, spider):
        collection = self.mongo_database[spider.name]
        collection.update_one(item, {'$set': item}, upsert=True)
        return item


class LeroymerlinImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        if item['images']:
            for image in item['images']:
                try:
                    yield scrapy.Request(image, meta=item)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        item = request.meta
        a = item["title"].replace("/", ":")
        return f'{a}/' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):

        item['characteristics'] = list(zip(item['terms'], item['definitions']))
        item['description'] = [i for i in item['description'] if i]
        item.pop('terms')
        item.pop('definitions')

        item['primary_price'] = price_procesing(item['primary_price'])
        item['second_price'] = price_procesing(item['second_price'])

        if results:
            item['images'] = [i[1] for i in results if i[0]]

        return item
