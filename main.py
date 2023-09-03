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

# returns full dictionary returned by spotify search
def get_spotify_search_results(list_of_albums):

    search_results = []
    
    for project in list_of_albums:
        search_results.append(sp.search(q = project, limit = 1, type = 'album'))

    return search_results

# returns search results simplified to artist: title
def get_available_albums(search_results):

    available_results = []

    for result in search_results:

        items = result['albums']['items']

        artist = items[0]['artists'][0]
        artist_name = artist['name']

        album = items[0]
        album_name = album['name']

        available_results.append(artist_name + ': ' + album_name)

        available_results = list(dict.fromkeys(available_results))

    return available_results

def get_uris(search_results):

    uris = []

    for result in search_results:

        uri = result['albums']['items'][0]['uri']
        uris.append(uri)

    return uris

house_search_results = get_spotify_search_results(house_artist_title)
grime_search_results = get_spotify_search_results(grime_artist_title)

house_available_albums = get_available_albums(house_search_results)
grime_available_albums = get_available_albums(grime_search_results)

house_uris = get_uris(house_search_results)
grime_uris = get_uris(grime_search_results)

print(house_uris[0])

#print(fuzz.ratio(house_artist_title[1], house_available_albums[1]))

# def compare_lists(hardwax_scrape, spotify_search_results):