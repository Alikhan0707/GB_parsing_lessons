from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
import re

a = input("Введите свой запрос: ")

main_link = 'https://hh.ru'
search_link = '/search/vacancy'

params = {
    'L_save_area': 'true',
    'clusters': 'true',
    'enable_snippets': 'true',
    'text': a,
    'showClusters': 'true'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': '*/*'
}

url = f'{main_link}{search_link}'
vacancies = []

while True:

    if '?' in url:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url, params=params, headers=headers)

    soup = bs(response.text, 'lxml')
    vacancies_block = soup.find('div', {'class': 'vacancy-serp'})
    vacancies_list = vacancies_block.findChildren(recursive=False)

    for vacancy in vacancies_list:

        if 'vacancy-serp-item' in vacancy.attrs['class']:

            vacancies_data = {}

            vacancy_info = vacancy.find('div', {'class': 'vacancy-serp-item__info'}).findChild('a')

            a = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).findChild()

            title = vacancy_info.text
            vacancy_link = vacancy_info['href']
            resource_link = main_link

            if a:
                salary = a.text.replace('\xa0', '')
                salary = re.findall(r'\w+', salary)
                currency = salary[-1]

                if 'от' in salary:

                    salary_min = salary[1]
                    salary_max = None

                elif 'до' in salary:

                    salary_max = salary[1]
                    salary_min = None

                else:

                    salary_min = salary[0]
                    salary_max = salary[1]
            else:

                salary_max = None
                salary_min = None
                currency = None

            vacancies_data['title'] = title
            vacancies_data['salary_min'] = salary_min
            vacancies_data['salary_max'] = salary_max
            vacancies_data['currency'] = currency
            vacancies_data['vacancy_link'] = vacancy_link
            vacancies_data['resource_link'] = resource_link
            vacancies.append(vacancies_data)

    next_button = soup.find('a', {'data-qa': 'pager-next'})

    if next_button:
        url = main_link + next_button['href']
    else:
        break

print(vacancies, '\n', len(vacancies))
