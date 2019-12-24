import requests, json, pprint

from config import MB_URL, MB_USER_AGENT

label_name = 'sahel sounds'

"""Define the paramaters and headers."""

params = {
    'query': label_name,
    'limit': 200,
    'fmt': 'json',
}

headers = {
  'User-Agent': MB_USER_AGENT,
}

response = requests.request("GET", MB_URL, params=params, headers=headers)

data = response.json()

mod = data['releases']

with open('json.txt', 'w') as f:
    json.dump(data, f)

"""Find title."""
title_list = [release['title'] for release in mod]

"""Find the artist."""
for release in mod:
    for item in release['artist-credit']:
        print(item['name'])

