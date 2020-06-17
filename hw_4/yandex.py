import requests
from lxml import html
from pprint import pprint
from datetime import datetime

main_link = 'https://yandex.kz/news/'
yandex = 'https://yandex.kz'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
blocks = dom.xpath("//div[@aria-labelledby='politics']//td[contains(@class, 'stories-set__item')]")

news_list = []

for block in blocks:
    news = {}
    title = block.xpath(".//a[contains(@class, 'link_theme_black')]/text()")
    link = block.xpath(".//a[contains(@class, 'link_theme_black')]/@href")
    date_and_resource = block.xpath(".//div[contains(@class, 'story__date')]/text()")
    dr = date_and_resource[0].split(' ')
    date = str(datetime.now().date()) + ' ' + dr[-1:][0]
    resource = ' '.join(map(str, dr[:-1]))
    news['title'] = title[0]
    news['resource'] = resource
    news['date_time'] = date
    news['link'] = yandex + link[0]
    news_list.append(news)

