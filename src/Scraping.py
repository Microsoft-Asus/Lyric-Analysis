import pandas as pd
from pymongo import MongoClient


def get_urls(artists_object, url_list):
    """
    INPUT: Mongo collections object
    OUTPUT: None

    This function takes in a mongo collection with the keys being the id and artists and the values are JSON objects. It
    then removes the id key. With that new collection, the function then indexes into the JSON object to retrieve the
    urls.
    """
    for artists in artists_object:
        info = list(artists.keys())
        info.remove('_id')
        for song in artists[info[0]]['response']['hits']:
            url_list.append(song['result']['url'])

def genius_scrape():
    pass


if __name__ == '__main__':

    '''
    Load MongoDB client
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.genius
    genius = db.genius

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
    urls = []
    get_urls(artists_songs, urls)