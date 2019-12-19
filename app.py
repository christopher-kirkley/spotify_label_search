from flask import Flask
from flask import render_template
import requests
import json
import spotipy
from requests_oauthlib import OAuth1


"""Initialize the app."""
app = Flask(__name__)

token = "BQC7c_UeAWvm4gP8NvyK0rOaCSXjQrvKrkKlFNfrYlEeChNzsZxhFYJiARAapCxAOYKfrqOMGIIAz5p_zWPq1n6xu25Y-6R0jjZhSMnfokOOBEQ5iE5GnioL4obthBbHoknq9Qn1QKl7oFyo'"

"""Set artist list from label"""
artist_list = ['Mamman Sani', 'Les Filles de Illighadad', 'Mdou Moctar', 'Luka Productions']


for artist in artist_list:
    url = f"https://api.spotify.com/v1/search?q={artist}&type=album"

    payload = {}
    headers = {
      'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    result = response.json()

    """Parse the result."""
    for album in result['albums']['items']:
        for item in album['artists']:
            artist_id = item['id']
        for item in album['images']:
            if item['height'] == 300:
                print(item['url'])

    print(artist)
    print(artist_id)



# json.dumps((x), indent=4)
@app.route("/")
def index():

    return render_template('index.html')

# """Conditional."""
# if __name__ == '__main__':
#     app.run(debug=True)