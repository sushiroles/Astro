import configparser
import base64
import aiohttp
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *
	


config = configparser.ConfigParser()
config.read('tokens.ini')
client_id = config['tidal']['id']
client_secret = f'{config['tidal']['secret']}='



async def get_access_token(client_id: str, client_secret: str):
	credentials = f'{client_id}:{client_secret}'
	encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
	async with aiohttp.ClientSession() as session:
		api_url = 'https://auth.tidal.com/v1/oauth2/token'
		api_data = {'grant_type': 'client_credentials'}
		api_headers = {'Authorization': f'Basic {encoded_credentials}'}
		async with session.post(url = api_url, data = api_data, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				return json_response['access_token']
			else:
				return ''
			
def is_tidal_track(url: str):
	return bool(url.find('https://tidal.com/browse/track/') >= 0)

def is_tidal_album(url: str):
	return bool(url.find('https://tidal.com/browse/album/') >= 0)

def get_tidal_track_id(url: str):
	return str(url.replace('https://tidal.com/browse/track/','').replace('?u',''))

def get_tidal_album_id(url: str):
	return str(url.replace('https://tidal.com/browse/album/','')).replace('?u','')



async def get_tidal_track(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://openapi.tidal.com/tracks/{identifier}?countryCode=US'
		api_headers = {
			'accept': 'application/vnd.api+json',
			'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}',
			'Content-Type': 'application/vnd.tidal.v1+json'
		}
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				track_url = json_response['resource']['tidalUrl']
				track_id = json_response['resource']['id']
				track_title = json_response['resource']['title']
				track_artists = [artist['name'] for artist in json_response['resource']['artists']]
				track_cover = json_response['resource']['album']['imageCover'][1]['url']
				return {
					'url': track_url,
					'id': track_id,
					'track': track_title,
					'artists': track_artists,
					'cover': track_cover,
				}
			else:
				return None
			


async def get_tidal_album(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://openapi.tidal.com/albums/{identifier}?countryCode=US'
		api_headers = {
			'accept': 'application/vnd.api+json',
			'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}',
			'Content-Type': 'application/vnd.tidal.v1+json'
		}
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				album_url = json_response['resource']['tidalUrl']
				album_id = json_response['resource']['id']
				album_title = json_response['resource']['title']
				album_artists = [artist['name'] for artist in json_response['resource']['artists']]
				album_cover = json_response['resource']['imageCover'][1]['url']
				return {
					'url': album_url,
					'id': album_id,
					'album': album_title,
					'artists': album_artists,
					'cover': album_cover,
				}
			else:
				return None	



async def search_tidal_track(artist: str, track: str):
	tracks_data = []
	async with aiohttp.ClientSession() as session:
		query = f'{artist} {track}'
		api_url = f"https://openapi.tidal.com/search?query={query}&type=TRACKS&offset=0&limit=30&countryCode=US&popularity=WORLDWIDE"
		api_headers = {
			'accept': 'application/vnd.api+json',
			'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}',
			'Content-Type': 'application/vnd.tidal.v1+json'
		}
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 207:
				json_response = await response.json()
				if json_response['tracks'] != []:
					for item in json_response['tracks']:
						track_url = item['resource']['tidalUrl']
						track_id = item['resource']['id']
						track_title = item['resource']['title']
						track_artists = [artist['name'] for artist in item['resource']['artists']]
						track_cover = item['resource']['album']['imageCover'][1]['url']
						tracks_data.append({
							'url': track_url,
							'id': track_id,
							'track': track_title,
							'artists': track_artists,
							'cover': track_cover,
						})
					return filter_track(artist = artist, track = track, tracks_data = tracks_data)
				else:
					return None
			else:
				return None



async def search_tidal_album(artist: str, album: str):
	albums_data = []
	async with aiohttp.ClientSession() as session:
		query = f'{artist} {album}'
		api_url = f"https://openapi.tidal.com/search?query={query}&type=ALBUMS&offset=0&limit=30&countryCode=US&popularity=WORLDWIDE"
		api_headers = {
			'accept': 'application/vnd.api+json',
			'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}',
			'Content-Type': 'application/vnd.tidal.v1+json'
		}
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 207:
				json_response = await response.json()
				if json_response['albums'] != []:
					for item in json_response['albums']:
						album_url = item['resource']['tidalUrl']
						album_id = item['resource']['id']
						album_title = item['resource']['title']
						album_artists = [artist['name'] for artist in item['resource']['artists']]
						album_cover = item['resource']['imageCover'][1]['url']
						albums_data.append({
							'url': album_url,
							'id': album_id,
							'album': album_title,
							'artists': album_artists,
							'cover': album_cover,
						})
					return filter_album(artist = artist, album = album, albums_data = albums_data)
				else:
					return None
			else:
				return None
