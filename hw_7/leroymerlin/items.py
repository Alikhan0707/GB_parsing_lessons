# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def cleaner_string(value: str):

    if '\n' in value:
        return value.replace('\n', '').strip()

    return value.strip()


def to_float(value: str):
    value = value.replace(' ', '')
    try:
        if value.isdigit():
            return int(value)
        else:
            return float(value)
    except ValueError:
        return value


class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:

    title = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    primary_price = scrapy.Field(input_processor=MapCompose(to_float))
    second_price = scrapy.Field(inpt_processor=MapCompose(to_float))
    description = scrapy.Field(input_processor=MapCompose(cleaner_string))
    terms = scrapy.Field(input_processor=MapCompose(cleaner_string))
    definitions = scrapy.Field(input_processor=MapCompose(cleaner_string, to_float))
    characteristics = scrapy.Field()

