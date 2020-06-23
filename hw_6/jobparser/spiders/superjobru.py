# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from hw_6.jobparser.items import SuperjobparserItem
import json


def correct_list(list_to_correct: list) -> list:
    corrected = [i.strip().replace('\xa0', '') for i in list_to_correct if i not in ['', ' ', ',', ', ', ' ,', '\xa0']]

    for i in range(len(corrected)):
        if corrected[i][0] == ',':
            corrected[i] = corrected[i][2:]
    return corrected


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = None
        self.company_name = None
        self.address = None
        self.payment_type = None
        self.currency = None
        self.salary_max = None
        self.salary_min = None
        self.experience = None
        self.mode = None
        self.description = None
        self.link = None
        self.site = self.allowed_domains[0]

    def parse(self, response: HtmlResponse):

        next_page = response.css("a.f-test-button-dalshe::attr(href)").extract_first()
        vacancy_links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9')]/@href").extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacacy_parse)

        yield response.follow(next_page, callback=self.parse)

    def vacacy_parse(self, response: HtmlResponse):

        experience = response.xpath("//div/span/span/span[contains(@class, '_3mfro _1hP6a _2JVkc')]/text()").extract()

        for i in experience:
            if 'Опыт' in i:
                start_idx = i.find('от ')
                self.experience = i[start_idx:]

        json_data = response.xpath(
            "//div[contains(@class, 'f-test-vacancy-base-info')]//div[contains(@class, '_1Tjoc _3C60a Ghoh2 UGN79 _1XYex')]//script[contains(@type, 'application/ld+json')]/text()").extract_first()
        vacancy_data = json.loads(json_data)

        self.name = vacancy_data['title']
        self.company_name = vacancy_data['identifier']['name']
        self.link = vacancy_data['url']

        address = vacancy_data['jobLocation']['address']
        address = list(address.values())
        self.address = ', '.join(map(str, address[1:]))

        self.description = response.xpath(
            "//span[contains(@class, '_3mfro _2LeqZ _1hP6a _2JVkc _2VHxz _15msI')]/span//text()").extract()

        for i in range(len(self.description)):
            self.description[i] = self.description[i].replace('\n', '')
            self.description[i] = self.description[i].strip()

        self.description = [i for i in self.description if not '']
        self.description = '\n'.join(map(str, self.description))

        if 'baseSalary' in vacancy_data.keys():

            self.currency = vacancy_data['baseSalary']['currency']

            if 'minValue' in vacancy_data['baseSalary']['value'].keys():
                self.salary_min = vacancy_data['baseSalary']['value']['minValue']
            if 'maxValue' in vacancy_data['baseSalary']['value'].keys():
                self.salary_max = vacancy_data['baseSalary']['value']['maxValue']
            self.payment_type = vacancy_data['baseSalary']['value']['unitText']

        self.mode = vacancy_data['employmentType']

        yield SuperjobparserItem(name=self.name,
                                 company_name=self.company_name,
                                 address=self.address,
                                 salary_min=self.salary_min,
                                 salary_max=self.salary_max,
                                 currency=self.currency,
                                 payment_type=self.payment_type,
                                 experience=self.experience,
                                 mode=self.mode,
                                 description=self.description,
                                 link=self.link,
                                 site=self.site)
