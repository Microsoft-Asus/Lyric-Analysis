import warnings
warnings.filterwarnings('ignore')
import copy
import pandas as pd
import requests
from bs4 import BeautifulSoup
import string
import urllib


#Scrapping:

def get_soup(letter):
    req = requests.get("https://www.billboard.com/artists/{}".format(letter))
    return BeautifulSoup(req.content)
    return soup.find("table", class_='views-view-grid cols-4')


def get_table(soup):
    tab = soup.find("table", class_='views-view-grid cols-4')
    rows = tab.find_all("tr")
    return rows


def get_artists(table):

    artists = []

    for row in table:
        for col in row.find_all("td"):
            try:
                artists.append(col.find('span', {'class': 'field-content'}).text)
            except AttributeError:
                continue

    return artists


#Getting JSON Objects:

def create_session(token):
    session = requests.session()

    session.headers.update({
        "Authorization": "Bearer {}".format(token)
    })

    return session


if __name__ == '__main__':

    BASE_URL = "https://api.genius.com/{}"
    origin_URL = 'https://genius.com/artists/{}'

    alpha = string.ascii_lowercase

    all_artists = []

    search_session = create_session('XXD8nij5Ebt7za_0ezVQ-FEh2h2rMdiKCPWlQgnIt5BIdfUu31w6r_86sQsKcLtH')

    for letter in alpha:
        soup = get_soup(letter)
        table = get_table(soup)
        all_artists.extend(get_artists(table))
    with open('artists.csv', 'w') as f:
        for artists in all_artists:
            f.write(artists + '\n')

