import configparser
import base64
import requests
import json

config = configparser.ConfigParser()
config.read('tokens.ini')

def get_tidal_access_token(client_id, client_secret):
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
\

def search_tidal_track(artist, track):
    url = f"https://openapi.tidal.com/search?query={f'{artist}-{track}'}&type=TRACKS&offset=0&limit=1&countryCode=US&popularity=WORLDWIDE"

    headers = {
        "accept": "application/vnd.tidal.v1+json",
        "Authorization": f"Bearer {get_tidal_access_token(config['tidal']['id'], config['tidal']['secret'] + '=')}",
        "Content-Type": "application/vnd.tidal.v1+json"
    }
    response = requests.get(url, headers=headers)
    track_data = response.json()["tracks"][0]['resource']

    with open('haha.json', 'w', encoding='utf-8') as outfile: 
        json.dump(response.json(), outfile, indent=4)
    if response.status_code == 207:
        try:
            return {
			    'url': track_data['tidalUrl'],
			    'id': track_data['id'],
			    'artist_name': track_data['artists'][0]['name'],
			    'track_name': track_data['title'],
			    'cover_art': track_data['album']['imageCover'][1],
		    }
        except:
            return None

def search_tidal_album(artist, album):
    url = f"https://openapi.tidal.com/search?query={f'{artist}-{album}'}&type=ALBUMS&offset=0&limit=1&countryCode=US&popularity=WORLDWIDE"

    headers = {
        "accept": "application/vnd.tidal.v1+json",
        "Authorization": f"Bearer {get_tidal_access_token(config['tidal']['id'], config['tidal']['secret'] + '=')}",
        "Content-Type": "application/vnd.tidal.v1+json"
    }
    response = requests.get(url, headers=headers)
    album_data = response.json()["albums"][0]['resource']


    if response.status_code == 207:
        try:
            return {
			    'url': album_data['tidalUrl'],
			    'id': album_data['id'],
			    'artist_name': album_data['artists'][0]['name'],
			    'album_name': album_data['title'],
			    'cover_art': album_data['imageCover'][1],
		    }
        except:
            return None
