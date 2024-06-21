import configparser
import base64
import requests
import json
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *

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

    url = f"https://openapi.tidal.com/search?query={f'{artist}-{track}'}&type=TRACKS&offset=0&limit=10&countryCode=US&popularity=WORLDWIDE"

    headers = {
        "accept": "application/vnd.tidal.v1+json",
        "Authorization": f"Bearer {get_access_token(config['tidal']['id'], config['tidal']['secret'] + '=')}",
        "Content-Type": "application/vnd.tidal.v1+json"
    }
    response = requests.get(url, headers=headers)
    search_results = response.json()["tracks"]

    if response.status_code == 207:
        for result in search_results:
            tracks_data.append({
                'url': str(result['resource']['tidalUrl']),
                'id': str(result['resource']['id']),
                'artist_name': str(result['resource']['artists'][0]['name']),
                'track_name': str(result['resource']['title']),
                'cover_art': str(result['resource']['album']['imageCover'][1]['url']),
            })
        return filter_track(artist, track, tracks_data)
    else:
        return None
    


def search_tidal_album(artist, album):
    albums_data = []

    url = f"https://openapi.tidal.com/search?query={f'{artist}-{album}'}&type=ALBUMS&offset=0&limit=10&countryCode=US&popularity=WORLDWIDE"

    headers = {
        "accept": "application/vnd.tidal.v1+json",
        "Authorization": f"Bearer {get_access_token(config['tidal']['id'], config['tidal']['secret'] + '=')}",
        "Content-Type": "application/vnd.tidal.v1+json"
    }
    response = requests.get(url, headers=headers)
    search_results = response.json()["albums"]
    if response.status_code == 207:
        for result in search_results:
            albums_data.append({
			    'url': str(result['resource']['tidalUrl']),
			    'id': str(result['resource']['id']),
			    'artist_name': str(result['resource']['artists'][0]['name']),
			    'album_name': str(result['resource']['title']),
                'release_year': str(result['resource']['releaseDate'][:4]),
			    'cover_art': str(result['resource']['imageCover'][1]['url']),
		    })
        return filter_album(artist, album, albums_data)
    else:
        return None
