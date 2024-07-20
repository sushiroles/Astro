import configparser
import base64
import requests
try:
	from services.etc import *
	from services.filter import *
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

def is_tidal_track(url: str):
	return bool(url.find('https://tidal.com/browse/track/') >= 0)

def is_tidal_album(url: str):
	return bool(url.find('https://tidal.com/browse/album/') >= 0)

def get_tidal_track_id(url: str):
	return str(url.replace('https://tidal.com/browse/track/',''))

def get_tidal_album_id(url: str):
	return str(url.replace('https://tidal.com/browse/album/',''))



def search_tidal_track(artist, track):
	tracks_data = []

	url = f"https://openapi.tidal.com/search?query={f'{artist}-{track}'}&type=TRACKS&offset=0&limit=30&countryCode=US&popularity=WORLDWIDE"

	headers = {
		"accept": "application/vnd.tidal.v1+json",
		"Authorization": f"Bearer {get_access_token(config['tidal']['id'], config['tidal']['secret'] + '=')}",
		"Content-Type": "application/vnd.tidal.v1+json"
	}
	response = requests.get(url, headers=headers)
	search_results = response.json()['tracks']

	if response.status_code == 207:
		for result in search_results:
			url = str(result['resource']['tidalUrl'])
			identifier = str(result['resource']['id'])
			artists = []
			for names in result['resource']['artists']:
				artists.append(names['name'])
			title = str(result['resource']['title'])
			cover = str(result['resource']['album']['imageCover'][1]['url'])
			tracks_data.append({
				'url': url,
				'id': identifier,
				'artists': artists,
				'track': title,
				'cover': cover,
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
	search_results = response.json()['albums']
	if response.status_code == 207:
		for result in search_results:
			url = str(result['resource']['tidalUrl'])
			identifier = str(result['resource']['id'])
			artists = []
			for names in result['resource']['artists']:
				artists.append(names['name'])
			title = str(result['resource']['title'])
			cover = str(result['resource']['imageCover'][1]['url'])
			albums_data.append({
				'url': url,
				'id': identifier,
				'artists': artists,
				'album': title,
				'cover': cover,
			})
		return filter_album(artist, album, albums_data)
	else:
		return None



def get_tidal_track(identifier: str):
	url = f"https://openapi.tidal.com/tracks/{identifier}?countryCode=US"
	headers = {
		"accept": "application/vnd.tidal.v1+json",
		"Authorization": f"Bearer {get_access_token(config['tidal']['id'], config['tidal']['secret'] + '=')}",
		"Content-Type": "application/vnd.tidal.v1+json"
	}
	response = requests.get(url, headers=headers)
	result = response.json()

	if response.status_code == 200:
		url = str(result['resource']['tidalUrl'])
		identifier = str(result['resource']['id'])
		artists = []
		for names in result['resource']['artists']:
			artists.append(names['name'])
		title = str(result['resource']['title'])
		cover = str(result['resource']['album']['imageCover'][1]['url'])
		return {
			'url': url,
			'id': identifier,
			'artists': artists,
			'track': title,
			'cover': cover,
		}
	else:
		return None



def get_tidal_album(identifier: str):
	url = f"https://openapi.tidal.com/albums/{identifier}?countryCode=US"
	headers = {
		"accept": "application/vnd.tidal.v1+json",
		"Authorization": f"Bearer {get_access_token(config['tidal']['id'], config['tidal']['secret'] + '=')}",
		"Content-Type": "application/vnd.tidal.v1+json"
	}
	response = requests.get(url, headers=headers)
	result = response.json()

	if response.status_code == 200:
		url = str(result['resource']['tidalUrl'])
		identifier = str(result['resource']['id'])
		artists = []
		for names in result['resource']['artists']:
			artists.append(names['name'])
		title = str(result['resource']['title'])
		cover = str(result['resource']['imageCover'][1]['url'])
		return {
			'url': url,
			'id': identifier,
			'artists': artists,
			'album': title,
			'cover': cover,
		}
	else:
		return None
