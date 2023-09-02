# This file just contains the code that scrapes from hardwax. I separated it into its own file for simplicity's sake.

import requests
from bs4 import BeautifulSoup

# below is gathering information for the first "grime" downloads page

grime_url = "https://hardwax.com/grime/?focus=only_downloads&page=1"

grime_request = requests.get(grime_url)

soup = BeautifulSoup(grime_request.content, 'html.parser')

grime_h2_tags = soup.find_all('h2')

grime_artist_title = []

for tag in grime_h2_tags:
        grime_artist_title.append(tag.get_text())

grime_artist_title = list(dict.fromkeys(grime_artist_title))

# below is gathering information for the first "house" downloads page