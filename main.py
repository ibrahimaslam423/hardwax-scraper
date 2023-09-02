# This main file checks the hardwax scrape results and attempts to add them each to a spotify playlist.

from hardwax import grime_artist_title, house_artist_title
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api_secrets import CLIENT_ID, CLIENT_SECRET

redirect_uri = 'https://www.google.com/'

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=redirect_uri))

grime_json_data = []
house_json_data = []

for grime_project in grime_artist_title:
    grime_json_data.append(sp.search(grime_project, 1, 0, 'album', None))

for house_project in house_artist_title:
    house_json_data.append(sp.search(house_project, 1, 0, 'album', None))