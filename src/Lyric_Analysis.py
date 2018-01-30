import pandas as pd
import numpy as np
from pymongo import MongoClient
from collections import defaultdict
import pdb
import warnings
warnings.filterwarnings('ignore')


if __name__ == '__main__':

    '''
    Load Mongo:
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.genius
    artist_info = db.genius
    artists_urls = db.artists_url
    artists_urls_2 = db.artists_urls_2

    lyrics_df = pd.DataFrame(columns=['Artist', 'Lyrics_Raw'])

    art_keys = []
    art_values = []
    for arts in artists_urls_2.find():
        art_keys.append(list(arts.keys())[1])
        art_values.append(arts.values()[1])
        break

    lyrics_df['Artist'] = art_keys
    lyrics_df['Lyrics_Raw'] = art_values


