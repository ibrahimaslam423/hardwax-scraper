# This main file checks the hardwax scrape results and attempts to add them each to a spotify playlist.

from hardwax import grime_artist_title, house_artist_title
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api_secrets import CLIENT_ID, CLIENT_SECRET
from fuzzywuzzy import fuzz

redirect_uri = 'https://www.google.com/'

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=redirect_uri))

grime_search_results = [] # this holds the full returned dictionary values from the api call
grime_list = [] # this holds the artist: title string from what is actually on spotify

for grime_project in grime_artist_title:
    grime_search_results.append(sp.search(q = grime_project, limit = 1, type = 'album'))

for result in grime_search_results:
    items = result['albums']['items']

    artist = items[0]['artists'][0]
    artist_name = artist['name']

    album = items[0]
    album_name = album['name']

    grime_list.append(artist_name + ': ' + album_name)

for name1 in grime_list:
    for name2 in grime_artist_title:
        ratio = fuzz.ratio(name1, name2)
        if ratio > 50:
            items = 
    

#for json_entry in grime_json_data:
#    grime_search_results.append()