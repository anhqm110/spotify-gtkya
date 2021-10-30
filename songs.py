import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from random_song import *

import random

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


#get random song


def get_rand_search():
    args = sys.argv[1:]
    n_args = len(args)
    access_token = get_token()
    
    try: 
        with open('genres.json', 'r') as infile:
            valid_genres = json.load(infile)
    except FileNotFoundError:
        print("Whahh")
        sys.exit(1)

    if n_args == 0:
        selected_genre = random.choice(valid_genres)
    else:
        selected_genre = (" ".join(args)).lower()
    
    if selected_genre in valid_genres:
        result = request_valid_song(access_token, genre=selected_genre)
        print(result)
    else:
        # If genre not found as it is, try fuzzy search with Levenhstein distance 2
        valid_genres_to_text = " ".join(valid_genres)
        try:
            closest_genre = find_near_matches(selected_genre, valid_genres_to_text,  max_l_dist=2)[0].matched
            result = request_valid_song(access_token, genre=closest_genre)
            print(result)
        except IndexError:
            print("Genre not found")

#take a list of songs and get the center


get_rand_search()

