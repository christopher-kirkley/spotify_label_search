import requests, json, pprint
from config import USER_AGENT, DISCOGS_KEY, DISCOGS_SECRET

"""Prompt user for label input."""
label = input('Enter a label: ')

"""Create the search for albums on label."""
url = f"https://api.discogs.com/database/search?label={label}&user-agent={USER_AGENT}&key={DISCOGS_KEY}&secret={DISCOGS_SECRET}"

"""Send request and get data from API, returning list ('Artists - Album')"""
response = requests.request("GET", url)
data = response.json() # Convert to JSON

"""Create blank dictionary."""
catalog = {}

"""Iterate over the result, creating dictionary of artists."""
for item in data['results']:
    title, catalog_id, image = item['title'], item['catno'], item['cover_image']
    artist, album = title.split(" - ", 1)
    """Create dictionary of artists."""
    catalog[artist] = []

"""Iterate over dictionary of artists, iterate over json and created nested lists of albums."""
for entry in catalog:
    for item in data['results']:
        title = item['title']
        artist, album = title.split(" - ", 1)
        if artist == entry:
            catalog[artist].append(album)

