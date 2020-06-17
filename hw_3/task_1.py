from hw_2 import task_1
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('192.168.8.105', 27017)
db = client['vacancies_db']

vacancies_db = db.vacancies

for vacancy in task_1.vacancies:
    vacancies_db.update_one(vacancy, {'$set': vacancy}, upsert=True)

salary_min = int(input('Введите минимальную зарабатную плату: '))

for vac in vacancies_db.find({'$or': [{'salary_min': {'$gte': salary_min}},
                                       {'salary_max': {'$lte': salary_min}}]}):
    pprint(vac)
