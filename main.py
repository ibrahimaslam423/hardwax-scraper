# This main file checks the hardwax scrape results and attempts to add them each to a spotify playlist.

from hardwax import artist_title
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api_secrets import CLIENT_ID, CLIENT_SECRET

redirect_uri = 'https://www.google.com/'

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=redirect_uri))

print(artist_title[6])

# result = sp.search(artist_title[6])

# print(result)