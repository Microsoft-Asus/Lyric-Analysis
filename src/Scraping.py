import pandas as pd
from pymongo import MongoClient
from pymongo.cursor import CursorType
import copy
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pdb
import warnings
warnings.filterwarnings('ignore')


def get_urls(artists_object):
    """
    INPUT: Mongo collections object
    OUTPUT: None

    This function takes in a mongo collection with the keys being the id and artists and the values are JSON objects. It
    then removes the id key. With that new collection, the function then indexes into the JSON object to retrieve the
    urls.
    """

    url_list = defaultdict(list)

    for artists in artists_object:
        info = list(artists.keys())
        info.remove('_id')

        try:
            for song in artists[info[0]]['response']['hits']:
                a = song['result']['url']
                url_list[info[0]].append(a)

        except (KeyError, TypeError) as e:
            continue

    return url_list


def add_dict_to_mongo(dictionary):
    """
    INPUT: Dictionary, Mongo colleciton
    OUTPUT: Mongo Collection

    This function takes in a dictionary (in my case {artists: url requests) and loads it into mongo in a collection.
    """

    artists_urls_2.insert_one(dictionary)


def get_soup(url):
    """
    INPUT: url
    OUTPUT: html

    This function takes in a url and returns the html of the url.
    """

    req = requests.get(url)
    soup = BeautifulSoup(req.content)
    try:
        div = soup.find("div", {"class": "lyrics"}).get_text()
        return div
    except:
        pass


def in_dict(value, dictionary):
    for v in dictionary.values():
        if value in v:
            return True
        return False

def get_lyrics(collection):

    divs = list(collection.values())
    soup = BeautifulSoup(divs)
    div_lyrics = soup.find("div", {"class": "lyrics"})


if __name__ == '__main__':

    '''
    Load MongoDB client
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.genius
    artist_info = db.genius
    artists_urls = db.artists_url
    artists_urls_2 = db.artists_urls_2

    '''
    Put the artists from artists.csv into a list.
    '''
    billboard_artists = []

    with open('artists.csv') as f:
        for artist in f:
            billboard_artists.append(artist)

    '''
    Get urls of the lyrics to the top songs from the artists
    '''
    artists_songs = artist_info.find()
    #pdb.set_trace()
    urls = get_urls(artists_songs)

    soups_list = []
    # import pdb; pdb.set_trace()
    for artist, url_list in urls.items():
        if artists_urls.find_one({artist:{"$exists":1}}):
            continue

        artists_soups = defaultdict(list)

        for url in url_list:
            if in_dict(get_soup(url), artists_soups):
                continue
            else:
                artists_soups[artist].append(get_soup(url))

        artists_soups_dict = dict(artists_soups)
        add_dict_to_mongo(artists_soups_dict)
