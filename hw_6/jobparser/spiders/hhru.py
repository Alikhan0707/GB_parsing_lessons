# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from hw_6.jobparser.items import JobparserItem


def correct_list(list_to_correct: list) -> list:
    corrected = [i.strip().replace('\xa0', '') for i in list_to_correct if i not in ['', ' ', ',', ', ', ' ,', '\xa0']]

    for i in range(len(corrected)):
        if corrected[i][0] == ',':
            corrected[i] = corrected[i][2:]
    return corrected


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&only_with_salary=true&salary=260000&from=cluster_compensation&showClusters=true']

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
        self.accept_handicapped = None
        self.key_skills = None
        self.link = None
        self.site = self.allowed_domains[0]

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next.HH-Pager-Control::attr(href)').extract_first()

        vacancy_links = response.css('div.vacancy-serp div.vacancy-serp-item a.HH-LinkModifier::attr(href)').extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacacy_parse)

        yield response.follow(next_page, callback=self.parse)

    def salary_parse(self, salary_job):
        if 'от' and 'до' in salary_job:
            self.salary_min = salary_job[1]
            self.salary_max = salary_job[3]
            self.currency = salary_job[4]
            self.payment_type = ''.join(map(str, salary_job[5:]))

        elif 'от' in salary_job:
            self.salary_min = salary_job[1]
            self.salary_max = None
            self.currency = salary_job[2]
            self.payment_type = ''.join(map(str, salary_job[3:]))

        elif 'до' in salary_job:
            self.salary_min = None
            self.salary_max = salary_job[1]
            self.currency = salary_job[2]
            self.payment_type = ' '.join(map(str, salary_job[3:]))

    def vacacy_parse(self, response: HtmlResponse):

        self.name = response.xpath('//h1/text()').extract_first()
        salary_job = response.css('p.vacancy-salary span::text').extract()
        salary_job = correct_list(salary_job)
        self.salary_parse(salary_job=salary_job)
        self.link = response._get_url()
        self.company_name = response.xpath("//div[contains(@class, 'vacancy-company-name-wrapper')]//text()").extract()

        if len(self.company_name) > 1:
            self.company_name = ' '.join(map(str, correct_list(self.company_name)))
        else:
            self.company_name = self.company_name[0]

        self.address = response.xpath("//p[contains(@data-qa, 'vacancy-view-location')]//text()").extract()

        if len(self.address) > 1:
            self.address = ', '.join(map(str, correct_list(self.address)))
        else:
            self.address = self.address[0]

        vacancy_description = response.xpath("//div[@class='vacancy-description']")
        self.experience = vacancy_description.xpath("//span[@data-qa='vacancy-experience']/text()").extract_first()
        self.mode = vacancy_description.xpath("//p[@data-qa='vacancy-view-employment-mode']//text()").extract()
        self.mode = correct_list(self.mode)

        vacancy_desc_sections = vacancy_description.xpath("//div[@class='vacancy-section']")
        self.description = vacancy_desc_sections[0].xpath("//div[@data-qa='vacancy-description']//text()").extract()
        self.description = correct_list(self.description)
        self.description = '\n'.join(map(str, self.description))

        self.accept_handicapped = vacancy_desc_sections[1].xpath("//span[@xpath='1']//text()").extract()

        if not self.accept_handicapped:
            self.accept_handicapped = None

        self.key_skills = vacancy_desc_sections[2].xpath(
            "//span[contains(@class, 'bloko-tag__section_text')]/text()").extract()
        self.key_skills = correct_list(self.key_skills)

        yield JobparserItem(name=self.name,
                            company_name=self.company_name,
                            address=self.address,
                            salary_min=self.salary_min,
                            salary_max=self.salary_max,
                            currency=self.currency,
                            payment_type=self.payment_type,
                            experience=self.experience,
                            mode=self.mode,
                            description=self.description,
                            accept_handicapped=self.accept_handicapped,
                            key_skills=self.key_skills,
                            link=self.link,
                            site=self.site)
