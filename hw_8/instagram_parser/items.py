# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class FollowersItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(output_processor=TakeFirst())
    user_id = scrapy.Field(output_processor=TakeFirst())
    username = scrapy.Field(output_processor=TakeFirst())
    full_name = scrapy.Field(output_processor=TakeFirst())
    profile_image = scrapy.Field(output_processor=TakeFirst())
    is_private = scrapy.Field(output_processor=TakeFirst())
    user_data = scrapy.Field(output_processor=TakeFirst())
    follower_username = scrapy.Field(output_processor=TakeFirst())
    follow_username = scrapy.Field(output_processor=TakeFirst())
