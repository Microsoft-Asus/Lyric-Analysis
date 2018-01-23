import pandas as pd
from pymongo import MongoClient
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

    try:
        for artists in artists_object:
            info = list(artists.keys())
            info.remove('_id')
            for song in artists[info[0]]['response']['hits']:
                s = song['result']['url']
                url_list[info[0]].append(s)
        return url_list
    except:
        pdb.set_trace()


def add_dict_to_mongo(dictionary):
    """
    INPUT: Dictionary, Mongo colleciton
    OUTPUT: Mongo Collection

    This function takes in a dictionary (in my case {artists: url requests) and loads it into mongo in a collection.
    """

    return artists_urls.insert_one(dictionary)


def get_soup(url):
    """
    INPUT: url
    OUTPUT: html

    This function takes in a url and returns the html of the url.
    """

    req = requests.get(url)
    return req
    #soup = BeautifulSoup(req.content)
    #div = soup.find("div", {"class": "lyrics"})
    #return div


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
    genius = db.genius
    artists_urls = db.artists_url

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
    artists_songs = genius.find()
    #pdb.set_trace()
    urls = get_urls(artists_songs)

    soups_list = []
    # import pdb; pdb.set_trace()
    for artist, url_list in urls.items():
        artists_soups = defaultdict(list)

        for url in url_list:
            artists_soups[artist].append(get_soup(url).content)
            break

        artists_soups_dict = dict(artists_soups)
        add_dict_to_mongo(artists_soups_dict)
        break

