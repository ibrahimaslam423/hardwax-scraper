# This main file checks the hardwax scrape results and attempts to add them each to a spotify playlist.

from hardwax import get_artist_title
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api_secrets import CLIENT_ID, CLIENT_SECRET
from fuzzywuzzy import fuzz

redirect_uri = 'https://www.google.com/'

# I am using all scopes because I am lazy and don't want to read the docs...
scopes = [
  'ugc-image-upload',
  'user-read-playback-state',
  'user-modify-playback-state',
  'user-read-currently-playing',
  'streaming',
  'app-remote-control',
  'user-read-email',
  'user-read-private',
  'playlist-read-collaborative',
  'playlist-modify-public',
  'playlist-read-private',
  'playlist-modify-private',
  'user-library-modify',
  'user-library-read',
  'user-top-read',
  'user-read-playback-position',
  'user-read-recently-played',
  'user-follow-read',
  'user-follow-modify'
]

grime_url = 'https://hardwax.com/grime/?focus=only_downloads&page=1'
grime_playlist_id = '4FLw6LbifCpach5rATQ1CY'

house_url = 'https://hardwax.com/house/?focus=only_downloads&page=1'
house_playlist_id = '6F0cDs13kULba4tV5fGlqi'

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=redirect_uri, scope = scopes))

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

# returns uris from spotify search results. For use in adding music to playlist
def get_uris(search_results):

    uris = []

    for result in search_results:

        uri = result['albums']['items'][0]['uri']
        uris.append(uri)

    return uris

# this function adds all songs from a particular album uri to a playlist
def add_songs(album_uris, playlist_id):

    for uri in album_uris:

        tracks = sp.album_tracks(uri)
        track_uris = [track['uri'] for track in tracks['items']]
        sp.playlist_add_items(playlist_id, track_uris)

# this function is kinda the main one - it compares values between scraped titles
# and searched titles, then adds songs if they are a close enough match (> 90% similar in fuzz ratio)
def compare_lists(hardwax_scrape, spotify_search_results, album_uris, playlist_id):
    for index1, element1 in enumerate(hardwax_scrape):
        for index2, element2 in enumerate(spotify_search_results):
            if (fuzz.ratio(element1, element2) > 90):
                add_songs(album_uris[index1], playlist_id)

house_search_results = get_spotify_search_results(house_artist_title)
grime_search_results = get_spotify_search_results(grime_artist_title)

house_available_albums = get_available_albums(house_search_results)
grime_available_albums = get_available_albums(grime_search_results)

house_album_uris = get_uris(house_search_results)
grime_album_uris = get_uris(grime_search_results)

compare_lists(house_artist_title, house_available_albums, house_album_uris, house_playlist_id)