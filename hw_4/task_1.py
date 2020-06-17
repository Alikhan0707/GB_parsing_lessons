from pymongo import MongoClient
from pprint import pprint
from hw_4 import yandex, mail_ru, lenta_ru

yandex_news = yandex.news_list
mail_ru_news = mail_ru.news_list
lenta_ru_news = lenta_ru.news_list

news_list = yandex_news + mail_ru_news + lenta_ru_news

client = MongoClient('192.168.8.105', 27017)
db = client['news_db']

news_collection = db.news

for news in news_list:
    news_collection.update_one(news, {'$set': news}, upsert=True)

for news in news_collection.find({}):
    pprint(news)