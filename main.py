import requests
from bs4 import BeautifulSoup

url = "https://hardwax.com/grime/?focus=only_downloads&page=1"

r = requests.get(url)

print(r.content[:100])

soup = BeautifulSoup(r.content, 'html.parser')
rows = soup.select('rm')