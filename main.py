# This main file checks the hardwax scrape results and attempts to add them each to a spotify playlist.

from hardwax import get_artist_title
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api_secrets import CLIENT_ID, CLIENT_SECRET
from fuzzywuzzy import fuzz
import requests
from bs4 import BeautifulSoup

redirect_uri = 'https://www.google.com/'

# necessary scopes
scopes = [
  'playlist-modify-public',
  'playlist-read-private',
  'playlist-modify-private'
]

grime_url = 'https://hardwax.com/grime/?focus=only_downloads&page=1'
grime_playlist_id = '4FLw6LbifCpach5rATQ1CY'

house_url = 'https://hardwax.com/house/?focus=only_downloads&page=1'
house_playlist_id = '6F0cDs13kULba4tV5fGlqi'

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri = redirect_uri, scope = scopes))

house_artist_title = get_artist_title(house_url)
grime_artist_title = get_artist_title(grime_url)

# this function gets information from the downloads page
def get_artist_title(url):
    
    request = requests.get(url)

    soup = BeautifulSoup(request.content, 'html.parser')

    h2_tags = soup.find_all('h2')

    artist_title = []

    for tag in h2_tags:
        artist_title.append(tag.get_text())

    artist_title = list(dict.fromkeys(artist_title)) # removes duplicate results by converting to dict then back to list

    return artist_title

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
def add_songs(album_uri, playlist_id):

    tracks = sp.album_tracks(album_uri)
    track_uris = [track['uri'] for track in tracks['items']]
    sp.playlist_add_items(playlist_id, track_uris)

# function to clear playlist before adding new tracks
def clear_playlist(playlist_id):
    results = sp.playlist_tracks(playlist_id)  
    tracks = results['items']  
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    track_chunks = [tracks[i:i+100] for i in range(0, len(tracks), 100)]

    for chunk in track_chunks:
        track_uris = [track['track']['uri'] for track in chunk]
        sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)
    
# this function is kinda the main one - it compares values between scraped titles
# and searched titles, then adds songs if they are a close enough match (== 100% match in fuzz ratio)
def compare_lists(hardwax_scrape, spotify_search_results, album_uris, playlist_id):

    for index, element1 in enumerate(hardwax_scrape):

        for index, element2 in enumerate(spotify_search_results):

            if (fuzz.ratio(element1, element2) == 100):
                add_songs(album_uris[index], playlist_id)
                print(element1, element2, album_uris[index])

def main():
    house_search_results = get_spotify_search_results(house_artist_title)
    grime_search_results = get_spotify_search_results(grime_artist_title)

    house_available_albums = get_available_albums(house_search_results)
    grime_available_albums = get_available_albums(grime_search_results)

    house_album_uris = get_uris(house_search_results)
    grime_album_uris = get_uris(grime_search_results)

    clear_playlist(house_playlist_id)
    clear_playlist(grime_playlist_id)

    # adding house tracks
    compare_lists(house_artist_title, house_available_albums, house_album_uris, house_playlist_id)

    # adding grime tracks
    compare_lists(grime_artist_title, grime_available_albums, grime_album_uris, grime_playlist_id)

main()