# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class JobparserPipeline(object):

    def __init__(self):
        client = MongoClient('172.20.10.9', 27017)
        self.monog_base = client.vacancy_hh_scrapy

    def process_item(self, item, spider):

        collection = self.monog_base[spider.name]
        collection.update_one(item, {'$set': item}, upsert=True)
        collection.find(item)
        return item

    def __del__(self):
        pass