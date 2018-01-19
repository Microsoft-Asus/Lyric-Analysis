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

def get_search(artist):
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

    # alpha = string.ascii_lowercase
    #
    # song_session = create_session('XXD8nij5Ebt7za_0ezVQ-FEh2h2rMdiKCPWlQgnIt5BIdfUu31w6r_86sQsKcLtH')
    # artist_session = create_session('XXD8nij5Ebt7za_0ezVQ-FEh2h2rMdiKCPWlQgnIt5BIdfUu31w6r_86sQsKcLtH')
    # search_session = create_session('XXD8nij5Ebt7za_0ezVQ-FEh2h2rMdiKCPWlQgnIt5BIdfUu31w6r_86sQsKcLtH')
    #
    # #pprint.pprint(get_song(song_session, 378195))
    # pprint.pprint(get_search(search_session, ['Kendrick', 'Lamar']))

    '''
    PyMongo:
    '''
    # import pdb
    # pdb.set_trace()
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.genius
    genius = db.genius

    search_session = create_session('XXD8nij5Ebt7za_0ezVQ-FEh2h2rMdiKCPWlQgnIt5BIdfUu31w6r_86sQsKcLtH')

    with open('artists.csv') as f:
        for artist in f:
            info = get_search(artist)
            if info:
                insert_into_mongo(info, artist)
            else:
                with open('did-not-work.csv', 'w') as f:
                    f.write(artist + '\n')
