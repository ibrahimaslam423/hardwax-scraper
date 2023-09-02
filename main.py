# This main file checks the hardwax scrape results and attempts to add them each to a spotify playlist.

from hardwax import artist_title
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api_secrets import CLIENT_ID, CLIENT_SECRET

redirect_uri = 'https://www.google.com/'

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=redirect_uri))

json_data = []

json_data.append(sp.search(artist_title[0], 1, 0, 'album', None))

# for project in artist_title:
#     json_data.append(sp.search(project, 1, 0, 'album', None))

print(json_data)