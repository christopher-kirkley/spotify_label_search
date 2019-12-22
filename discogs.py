import requests, json, pprint
from config import USER_AGENT, DISCOGS_KEY, DISCOGS_SECRET

label = input('Enter a label: ')

url = f"https://api.discogs.com/database/search?label={label}&user-agent={USER_AGENT}&key={DISCOGS_KEY}&secret={DISCOGS_SECRET}"

response = requests.request("GET", url)

data = response.json() # Convert to JSON

album_list = []

for item in data['results']:
    title, catalog_id, image = item['title'], item['catno'], item['cover_image']
    artist_album = title.split(" - ", 1)
    album_list.append(artist_album)

print(album_list)