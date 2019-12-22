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

"""Initialize the app."""
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


"""Authorize the app."""
authorize_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

"""Set artist list from label"""
artist_list = ['Mamman Sani', 'Les Filles de Illighadad', 'Mdou Moctar', 'Luka Productions', 'Abba Gargando']

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

    """Loop over artist in artist list and return json of albums."""
    for artist in artist_list:
        album_data = {}
        url = f"https://api.spotify.com/v1/search?q={artist}&type=album"

        headers = {
                    'Authorization': f'Bearer {token}'
                    }

        response = requests.request("GET", url, headers=headers)

        albums_by_artist = response.json()

        """Parse the result."""
        for album in albums_by_artist['albums']['items']:
            images = []
            for entry in album['artists']:
                artist_id = entry['id']
            album_name = album['name']
            for entry in album['images']:
                if entry['height'] == 300:
                    album_data[album_name] = entry['url']
        artist_data[artist] = album_data

    return render_template('playlist.html', token=token, artist_data=artist_data)

"""Conditional."""
if __name__ == '__main__':
    app.run(debug=True)