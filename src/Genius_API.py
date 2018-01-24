import requests
import pprint
from bs4 import BeautifulSoup
import string
import urllib
from pymongo import MongoClient

# use a .format to set the path
BASE_URL = "https://api.genius.com/{}"
origin_URL = 'https://genius.com/artists/{}'


def get_soup(url, artist):
    req = requests.get(url.format(artist))
    return BeautifulSoup(req.content)
    return soup.find("class", class_='views-view-grid cols-4')


def create_session(token):
    session = requests.session()

    session.headers.update({
        "Authorization": "Bearer {}".format(token)
    })

    return session


def get_song(session, song_id):
    return session.get(BASE_URL.format('songs/{}'.format(song_id))).json()


def get_artist(session, artist_id):
    return session.get(BASE_URL.format('artists/{}'.format(artist_id))).json()


def get_search(artist, search_session):
    try:
        params = urllib.parse.urlencode({'artist': artist})
        return search_session.get(BASE_URL.format('search/?q={}'.format(artist))).json()
    except:
        return None


def insert_into_mongo(info, artist):
    genius.insert_one({
        artist.replace(".",'') : info
    })


if __name__ == '__main__':

    '''
    PyMongo:
    '''
    # import pdb
    # pdb.set_trace()
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.genius
    genius = db.genius

    search_session_1 = create_session('XXD8nij5Ebt7za_0ezVQ-FEh2h2rMdiKCPWlQgnIt5BIdfUu31w6r_86sQsKcLtH')
    search_session_2 = create_session('U2Xx7cZF6WQN9oMxU99VEqmT79mfnT5Jhg8SpMWbW_0hwXvkPa0SdmBlowi7KdPm')
    search_session_3 = create_session('TuRaQ1sW6bPvX7U9IQ0oIPDt9HVQytvBEtIkcIY4WgMR3uQ8JyJUewZvLHJsUdtl')
    search_session_4 = create_session('CWs-HZEbCRqYEJllxGfw_k9DH60UMPoZfmAwAinCgt4_MGMh6Mc89K26zjuzprgm')
    search_session_5 = create_session('0opw9AuoTvr75rFD7tF5ghdiPwwARY-UOrfSxDP25wFDpeWNyBqO_FZh3T5ZU2wM')

    sessions = [search_session_1, search_session_2, search_session_3, search_session_4, search_session_5]
    counter = 0
    with open('artists.csv') as f:
        for artist in f:
                info = get_search(artist, sessions[counter])
                counter +=1
                if counter >= 4:
                    counter = 0
                if info:
                    insert_into_mongo(info, artist)
                else:
                    with open('did-not-work.csv', 'w') as f:
                        f.write(artist + '\n')



    '''
    NOT SURE IF I WANT TO DELETE!!!!
    '''
    # import warnings
    #
    # warnings.filterwarnings('ignore')
    # import copy
    # import pandas as pd
    # import requests
    # from bs4 import BeautifulSoup
    # import string
    # import urllib
    #
    #
    # # Scrapping:
    #
    # def get_soup(letter):
    #     req = requests.get("https://www.billboard.com/artists/{}".format(letter))
    #     return BeautifulSoup(req.content)
    #     return soup.find("table", class_='views-view-grid cols-4')
    #
    #
    # def get_table(soup):
    #     tab = soup.find("table", class_='views-view-grid cols-4')
    #     rows = tab.find_all("tr")
    #     return rows
    #
    #
    # def get_artists(table):
    #
    #     artists = []
    #
    #     for row in table:
    #         for col in row.find_all("td"):
    #             try:
    #                 artists.append(col.find('span', {'class': 'field-content'}).text)
    #             except AttributeError:
    #                 continue
    #
    #     return artists
    #
    #
    # # Getting JSON Objects:
    #
    # def create_session(token):
    #     session = requests.session()
    #
    #     session.headers.update({
    #         "Authorization": "Bearer {}".format(token)
    #     })
    #
    #     return session
    #
    #
    # if __name__ == '__main__':
    #
    #     BASE_URL = "https://api.genius.com/{}"
    #     origin_URL = 'https://genius.com/artists/{}'
    #
    #     alpha = string.ascii_lowercase
    #
    #     all_artists = []
    #
    #     search_session = create_session('XXD8nij5Ebt7za_0ezVQ-FEh2h2rMdiKCPWlQgnIt5BIdfUu31w6r_86sQsKcLtH')
    #
    #     for letter in alpha:
    #         soup = get_soup(letter)
    #         table = get_table(soup)
    #         all_artists.extend(get_artists(table))
    #     with open('artists.csv', 'w') as f:
    #         for artists in all_artists:
    #             f.write(artists + '\n')