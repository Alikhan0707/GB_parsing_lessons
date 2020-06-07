import requests

a = input('Введите имя пользователя: ')

url = f'https://api.github.com/users/{a}/repos'

response = requests.get(url)

with open(f'{a}_repo_list.json', 'w') as f:
    f.write(response.text)
