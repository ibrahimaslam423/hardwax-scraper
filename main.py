import requests
from bs4 import BeautifulSoup

url = "https://hardwax.com/grime/?focus=only_downloads&page=1"

request = requests.get(url)

soup = BeautifulSoup(request.content, 'html.parser')

h2_tags = soup.find_all('h2')

text_tags = []

for tag in h2_tags:
    text_tags.append(tag.get_text())

print(text_tags)