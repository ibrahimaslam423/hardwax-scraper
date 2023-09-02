# This main file checks the hardwax scrape results and attempts to add them each to a spotify playlist.

import hardwax
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from api_secrets import CLIENT_ID, CLIENT_SECRET

redirect_uri = 'google.com'

credentials = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)

token = credentials.get_access_token()

spotify = spotipy.Spotify(auth=token)

uris = []