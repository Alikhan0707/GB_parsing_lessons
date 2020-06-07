import requests

api_key = '9a9cf3da7d514d7f91b7448ce3502cd7'

url = 'https://api.weatherbit.io/v2.0/forecast/agweather'

params = {
    'lat': '41.79',
    'lon': '68.48',
    'key': api_key,
    'unit': 'M'  # M, S, I
}

response = requests.get(url, params=params)

with open('weather.json', 'wb') as f:
    f.write(response.content)