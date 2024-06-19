import configparser
import base64
import requests
import json
from etc import *

config = configparser.ConfigParser()
config.read('tokens.ini')

def get_access_token(client_id, client_secret):
    credentials = f'{client_id}:{client_secret}'

    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    authorization_header = f'Basic {encoded_credentials}'
    data = {'grant_type': 'client_credentials'}

    response = requests.post(
        url='https://auth.tidal.com/v1/oauth2/token',
        headers={'Authorization': authorization_header},
        data=data,
    )
    return response.json()['access_token']


def search_tidal_track(artist, track):
    tracks_data = []

    url = f"https://openapi.tidal.com/search?query={f'{artist}-{track}'}&type=TRACKS&offset=0&limit=5&countryCode=US&popularity=WORLDWIDE"

    headers = {
        "accept": "application/vnd.tidal.v1+json",
        "Authorization": f"Bearer {get_access_token(config['tidal']['id'], config['tidal']['secret'] + '=')}",
        "Content-Type": "application/vnd.tidal.v1+json"
    }
    response = requests.get(url, headers=headers)
    search_results = response.json()["tracks"]

    if response.status_code == 207:
        for search_results_num in range(len(search_results)):
            tracks_data.append({
                'url': search_results[search_results_num]['resource']['tidalUrl'],
                'id': search_results[search_results_num]['resource']['id'],
                'artist_name': search_results[search_results_num]['resource']['artists'][0]['name'],
                'track_name': search_results[search_results_num]['resource']['title'],
                'cover_art': search_results[search_results_num]['resource']['album']['imageCover'][1]['url'],
            })
        return tracks_data
    else:
        return None
    


def search_tidal_album(artist, album):
    albums_data = []

    url = f"https://openapi.tidal.com/search?query={f'{artist}-{album}'}&type=ALBUMS&offset=0&limit=5&countryCode=US&popularity=WORLDWIDE"

    headers = {
        "accept": "application/vnd.tidal.v1+json",
        "Authorization": f"Bearer {get_access_token(config['tidal']['id'], config['tidal']['secret'] + '=')}",
        "Content-Type": "application/vnd.tidal.v1+json"
    }
    response = requests.get(url, headers=headers)
    search_results = response.json()["albums"]
    
    #with open('data.json', 'w', encoding='utf-8') as f:
    #    json.dump(search_results, f, ensure_ascii=False, indent=4)

    #return None
    if response.status_code == 207:
        for search_results_num in range(len(search_results)):
            albums_data.append({
			    'url': search_results[search_results_num]['resource']['tidalUrl'],
			    'id': search_results[search_results_num]['resource']['id'],
			    'artist_name': search_results[search_results_num]['resource']['artists'][0]['name'],
			    'album_name': search_results[search_results_num]['resource']['title'],
			    'cover_art': search_results[search_results_num]['resource']['imageCover'][1]['url'],
		    })
        return albums_data
    else:
        return None
