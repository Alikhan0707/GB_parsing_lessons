# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from hw_7.leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        product_links = response.xpath('//div[contains(@class, "plp-card-list-inner")]//a[contains(@class, "product-name")]')

        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response: HtmlResponse):

        loader = ItemLoader(item=LeroymerlinItem(), response=response)

        loader.add_xpath('images', '//img[@alt="product image"]/@src')
        loader.add_xpath('title', '//h1[@slot="title"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('primary_price', '//uc-pdp-price-view[contains(@slot, "primary-price")]/span/text()')
        loader.add_xpath('second_price', '//uc-pdp-price-view[contains(@slot, "second-price")]/span/text()')
        loader.add_xpath('description', '//section[contains(@class, "description")]//uc-pdp-section-vlimited/div//text()')
        loader.add_xpath('terms', '//section[contains(@class, "characteristicks")]//dt/text()')
        loader.add_xpath('definitions', '//section[contains(@class, "characteristicks")]//dd/text()')
        loader.add_value('characteristics', None)

        yield loader.load_item()
