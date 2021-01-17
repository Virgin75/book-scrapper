import requests
from bs4 import BeautifulSoup


r = requests.get("https://www.google.fr")
soup = BeautifulSoup(r.text, 'html.parser')

print(soup.title)
