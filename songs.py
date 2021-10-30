import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from random_song import *

import random

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

import numpy as np

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
    
    result = -1
    while (result == -1):
        if selected_genre in valid_genres:
            result = request_valid_song(access_token, genre=selected_genre)
            return result
        else:
            # If genre not found as it is, try fuzzy search with Levenhstein distance 2
            valid_genres_to_text = " ".join(valid_genres)
            try:
                closest_genre = find_near_matches(selected_genre, valid_genres_to_text,  max_l_dist=2)[0].matched
                result = request_valid_song(access_token, genre=closest_genre)
                return result
            except IndexError:
                print("song not found")

#gets song info

def get_song_info(song_id):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    
    uri = "spotify:track:" + song_id
    
    track = spotify.track(uri)
    
    return song_id, track['preview_url'], track['album']['images'][0]['url']

def get_rand_song():

    search = get_rand_search()
    return get_song_info(search)



            
#take a list of songs and get the center
def calculate_center(song_list):
    
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'
    
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    #acousticness, danceability, energy, instramentalness, loudness, tempo

    final_arr = np.zeros(6)

    for song in song_list:

        # actual GET request with proper header
        r = requests.get(BASE_URL + 'audio-features/' + song, headers=headers)
        
        r = r.json()

        add_arr = np.array([r['acousticness'], r['danceability'], r['energy'], r['instrumentalness'], r['loudness'], r['tempo']])
        
        final_arr += add_arr

    final_arr /= len(song_list)
    return final_arr


