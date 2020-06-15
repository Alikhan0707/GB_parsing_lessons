from hw_2 import task_1
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('192.168.8.106', 27017)
db = client['vacancies_db']

vacancies_db = db.vacancies

for vacancy in task_1.vacancies:
    if vacancy not in vacancies_db.find(vacancy):
        vacancies_db.insert_one(vacancy)

salary_min = int(input('Введите минимальную зарабатную плату: '))

for vac in vacancies_db.find({'salary_min': {'$gt': salary_min}}):
    pprint(vac)
