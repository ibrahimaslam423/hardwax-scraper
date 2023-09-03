# This file just contains the code that scrapes from hardwax. I separated it into its own file for simplicity's sake.

import requests
from bs4 import BeautifulSoup

# this function information from the downloads page

def get_artist_title(url):
    
    request = requests.get(url)

    soup = BeautifulSoup(request.content, 'html.parser')

    h2_tags = soup.find_all('h2')

    artist_title = []

    for tag in h2_tags:
        artist_title.append(tag.get_text())

    artist_title = list(dict.fromkeys(artist_title)) # removes duplicate results by converting to dict then back to list

    return artist_title