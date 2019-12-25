import requests, json, pprint

from config import MB_URL, MB_USER_AGENT

"""Get the MBID of the label."""

"""Make list of release-group items with MBID."""

def label_search(label_name):
    """Function to find releases by label on MusicBrainzAPI."""

    headers = {'User-Agent': MB_USER_AGENT} # Header defined

    """First find the MBID of the label."""
    url = f"https://musicbrainz.org/ws/2/label/?limit=200&query=label:\"{label_name}\"&fmt=json"
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    for item in data['labels']:
        label_id = item['id']

    """Lookup label releases by MBID of the label."""
    url = f"https://musicbrainz.org/ws/2/release?label={label_id}&fmt=json&limit=200&inc=artist-credits"
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    mod = data['releases']

    catalog = {}

    """Iterate over json, and create dictionary of artist, release."""
    for item in mod:
        title = item['title']
        for item in item['artist-credit']:
            artist = item['name']
            if artist not in catalog:
                catalog[artist] = []
                catalog[artist].append(title)
            else:
                catalog[artist].append(title)

    return catalog










