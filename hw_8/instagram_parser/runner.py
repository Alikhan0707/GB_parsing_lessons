from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from hw_8.instagram_parser.spiders.instagram import InstagramSpider
from hw_8.instagram_parser import settings
from pymongo import MongoClient
from pprint import pprint

if __name__ == "__main__":
    client = MongoClient('192.168.8.105', 27017)
    db = client['users_data']
    users_data = db[InstagramSpider.name]
    parse_users = [] # Исследуемые объекты - avtomirvtule, codemillz
    try:
        while True:
            username = input('Введите имя пользователя(-ей). Чтобы начать парсинг подписчиков (подписок) введите "0": ')
            if username == "0":
                break
            else:
                parse_users.append(username)
        crawler_settings = Settings()
        crawler_settings.setmodule(settings)

        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(InstagramSpider, parse_users=parse_users)
        process.start()
    finally:
        while True:
            user = input("Введите имя пользователя. Для выхода из цикла введите '0': ")
            if user == '0':
                break
            follow = input("Введите цифру '1' - подписчики, '2' - подписки. Для выхода из цикла введите '0': ")
            if follow == '0':
                break
            elif follow == '1':
                for data in users_data.find({'follow_username': user}):
                    pprint(data)
            elif follow == '2':
                for data in users_data.find({'follower_username': user}):
                    pprint(data)