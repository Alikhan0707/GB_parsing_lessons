import requests
from lxml import html
from pprint import pprint

main_link = 'https://lenta.ru'
resource = 'Lenta.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)

blocks = dom.xpath("//a[contains(@href, '/news/')]//time[@class='g-time']")

news_list = []

for block in blocks:
    news = {}
    datetime = block.xpath('./@datetime')
    datetime = datetime[0].strip()
    title = block.xpath('./../text()')
    title = title[0].replace('\xa0', ' ')
    link = block.xpath('./../@href')
    link = main_link + link[0]

    news['title'] = title
    news['resource'] = resource
    news['date_time'] = datetime
    news['link'] = link
    news_list.append(news)

