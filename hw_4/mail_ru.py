import requests
from lxml import html
from pprint import pprint
from datetime import datetime

main_link = 'https://news.mail.ru'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
news_list = []
blocks = dom.xpath("//div[contains(@class, 'link-hdr')]//a[@href='/economics/']/../../..")[0]
head_news_resource = blocks.xpath("//span[@class='newsitem__param']/text()")
head_news_date = blocks.xpath("//span[contains(@class, 'js-ago')]/@datetime")
head_news_date = head_news_date[0]
head_news_link = blocks.xpath("//a[contains(@class, 'newsitem__title')]/@href")
head_news_title = blocks.xpath("//span[contains(@class, 'newsitem__title')]/text()")
next_news_blocks = blocks.xpath("//li[contains(@class, 'list')]//a[contains(@class, 'link')]")

news_list.append({
    'resource': head_news_resource[0],
    'title': head_news_title[0],
    'date_time': head_news_date,
    'link': main_link + head_news_link[0]
})

for block in next_news_blocks:
    news = {}
    news_link = block.xpath('./@href')
    news_link = main_link + news_link[0]
    resp = requests.get(news_link, headers=headers)
    news_dom = html.fromstring(resp.text)
    title = news_dom.xpath("//div[contains(@class, 'article js-article')]//h1[@class='hdr__inner']/text()")
    resource = news_dom.xpath("//div[contains(@class, 'article js-article')]"
                              "//span[contains(@class, 'link__text')]/text()")
    date_time = news_dom.xpath("//div[contains(@class, 'article js-article')]"
                               "//span[contains(@class, 'js-ago')]/@datetime")
    news['title'] = title[0]
    news['resource'] = resource[0]
    news['date_time'] = date_time[0]
    news['link'] = news_link
    news_list.append(news)
