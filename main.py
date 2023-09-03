# This main file checks the hardwax scrape results and attempts to add them each to a spotify playlist.

from hardwax import get_artist_title
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api_secrets import CLIENT_ID, CLIENT_SECRET
from fuzzywuzzy import fuzz

redirect_uri = 'https://www.google.com/'
grime_url = 'https://hardwax.com/grime/?focus=only_downloads&page=1'
house_url = 'https://hardwax.com/house/?focus=only_downloads&page=1'

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=redirect_uri))

house_artist_title = get_artist_title(house_url)
grime_artist_title = get_artist_title(grime_url)

def spotify_search(list_of_albums):

    search_results = []
    available_results = []

    for project in list_of_albums:
        search_results.append(sp.search(q = project, limit = 1, type = 'album'))

    for result in search_results:

        items = result['albums']['items']

        artist = items[0]['artists'][0]
        artist_name = artist['name']

        album = items[0]
        album_name = album['name']

        available_results.append(artist_name + ': ' + album_name)

    return available_results

print(spotify_search(house_artist_title))