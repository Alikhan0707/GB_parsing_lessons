# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    company_name = scrapy.Field()
    address = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    currency = scrapy.Field()
    payment_type = scrapy.Field()
    experience = scrapy.Field()
    mode = scrapy.Field()
    description = scrapy.Field()
    accept_handicapped = scrapy.Field()
    key_skills = scrapy.Field()
    link = scrapy.Field()
    site = scrapy.Field()


class SuperjobparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    company_name = scrapy.Field()
    address = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    currency = scrapy.Field()
    payment_type = scrapy.Field()
    experience = scrapy.Field()
    mode = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    site = scrapy.Field()