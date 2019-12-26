from flask import Flask
from flask import render_template, url_for, request, redirect
import requests
import json
import spotipy
from requests_oauthlib import OAuth1

"""Import config variables."""
from config import CLIENT_ID
from config import AUTHORIZATION
from config import REDIRECT_URI

"""Import musicbrainz"""
from musicbrainz import label_search
catalog = label_search('Warp')

"""Initialize the app."""
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


"""Authorize the app."""
authorize_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        """Redirect to the authorization page."""
        return redirect(authorize_url)

    return render_template('index.html')

@app.route("/callback", methods=['GET', 'POST'])
def callback():
    """Callback from Spotify redirected url."""

    """Get code from URL."""
    code = request.args.get('code')

    """Initialize variables for token."""
    grant_type = 'authorization_code'

    """Make post request for token."""
    headers = {
                'Authorization': f'Basic {AUTHORIZATION}',
              }

    data = {
            'grant_type': 'authorization_code',
            'code': {code},
            'redirect_uri': 'http://localhost:5000/callback'
            }


    r = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    response = r.json()

    """Get access token."""
    token = response['access_token']

    return redirect(url_for('playlist', token=token))

@app.route("/playlist", methods=['GET', 'POST'])
def playlist():
    """Playlist view of artists from label."""
    token = request.args.get('token')

    artist_data = {}

    """Loop over catalog return json of albums."""
    for artist, albums in catalog.items():
        list = []
        for album in albums:
            """Set variables."""
            url = f"https://api.spotify.com/v1/search?q=album:'{album}' artist:'{artist}'&type=album"
            headers = {
                        'Authorization': f'Bearer {token}'
                        }

            """Get response from API, transform to json."""
            response = requests.request("GET", url, headers=headers)

            if response.status_code == 200:
                albums_by_artist = response.json()

                album_data = {}

                """Parse the result."""
                for albumjson in albums_by_artist['albums']['items']:
                    images = []
                    for entry in albumjson['artists']:
                        artist_id = entry['id']
                    album_name = albumjson['name']
                    for entry in albumjson['images']:
                        if entry['height'] == 300:
                            album_data[album_name] = entry['url']
                    list.append(album_data)
                artist_data[artist] = list
            else:
                pass

    return render_template('playlist.html', token=token, artist_data=artist_data)

"""Conditional."""
if __name__ == '__main__':
    app.run(debug=True)

#
#    # """Loop over artist in artist list and return json of albums."""
    # for artist in artist_list:
    #     album_data = {}
    #     url = f"https://api.spotify.com/v1/search?q={artist}&type=album"
    #
    #     headers = {
    #                 'Authorization': f'Bearer {token}'
    #                 }
    #
    #     response = requests.request("GET", url, headers=headers)
    #
    #     albums_by_artist = response.json()
    #
    #     """Parse the result."""
    #     for album in albums_by_artist['albums']['items']:
    #         images = []
    #         for entry in album['artists']:
    #             artist_id = entry['id']
    #         album_name = album['name']
    #         for entry in album['images']:
    #             if entry['height'] == 300:
    #                 album_data[album_name] = entry['url']
    #     artist_data[artist] = album_data
