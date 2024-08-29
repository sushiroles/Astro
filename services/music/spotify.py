import configparser
import aiohttp
import asyncio
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *



config = configparser.ConfigParser()
config.read('tokens.ini')
client_id = config['spotify']['id']
client_secret = config['spotify']['secret']


async def get_access_token(client_id: str, client_secret: str):
	async with aiohttp.ClientSession() as session:
		api_url = 'https://accounts.spotify.com/api/token'
		api_data = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
		api_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		async with session.post(url = api_url, data = api_data, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				return json_response['access_token']
			else:
				return ''

def is_spotify_track(url: str):
	return bool(url.find('https://open.spotify.com/track/') >= 0)
	
def is_spotify_album(url: str):
	return bool(url.find('https://open.spotify.com/album/') >= 0)

def get_spotify_id(url: str):
	return url[31:53]



async def get_spotify_track(identifier: str):
	start_time = current_time_ms()
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.spotify.com/v1/tracks/{identifier}'
		api_headers = {'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}'}
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				track_url = json_response['external_urls']['spotify']
				track_id = json_response['id']
				track_title = json_response['name']
				track_artists = [artist['name'] for artist in json_response['artists']]
				track_cover = json_response['album']['images'][0]['url']
				track_collection = json_response['album']['name']
				track_is_explicit = json_response['explicit']
				return {
					'type': 'track',
					'url': track_url,
					'id': track_id,
					'title': track_title,
					'artists': track_artists,
					'cover': track_cover,
					'collection_name': track_collection,
					'is_explicit': track_is_explicit,
					'extra': {
						'time_ms': current_time_ms() - start_time,
						'response_status': f'Spotify-{response.status}'
					}
				}
			else:
				return {
					'type': 'error',
					'response_status': f'Spotify-{response.status}'
				}



async def get_spotify_album(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.spotify.com/v1/albums/{identifier}'
		api_headers = {'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}'}
		start_time = current_time_ms()
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				album_url = json_response['external_urls']['spotify']
				album_id = json_response['id']
				album_title = json_response['name']
				album_artists = [artist['name'] for artist in json_response['artists']]
				album_cover = json_response['images'][0]['url']
				album_year = json_response['release_date'][:4]
				return {
					'type': 'album',
					'url': album_url,
					'id': album_id,
					'title': album_title,
					'artists': album_artists,
					'cover': album_cover,
					'year': album_year,
					'extra': {
						'api_time_ms': current_time_ms() - start_time,
						'response_status': f'Spotify-{response.status}'
					}
				}
			else:
				return {
					'type': 'error',
					'response_status': f'Spotify-{response.status}'
				}
			


async def search_spotify_track(artist: str, track: str, collection: str = None, is_explicit: bool = None):
	tracks_data = []
	async with aiohttp.ClientSession() as session:
		query = f'artist:{artist} track:{track}'
		api_url = f'https://api.spotify.com/v1/search?q={query}&type=track&limit=50'
		api_headers = {'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}'}
		start_time = current_time_ms()
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				if json_response['tracks']['items']:
					for item in json_response['tracks']['items']:
						track_url = item['external_urls']['spotify']
						track_id = item['id']
						track_title = item['name']
						track_artists = [artist['name'] for artist in item['artists']]
						track_cover = item['album']['images'][0]['url']
						track_collection = item['album']['name']
						track_is_explicit = item['explicit']
						tracks_data.append({
							'type': 'track',
							'url': track_url,
							'id': track_id,
							'title': track_title,
							'artists': track_artists,
							'cover': track_cover,
							'collection_name': track_collection,
							'is_explicit': track_is_explicit,
							'extra': {
								'api_time_ms': current_time_ms() - start_time,
								'response_status': f'Spotify-{response.status}'
							}
						})
					return filter_track(tracks_data = tracks_data, artist = artist, track = track, collection = collection, is_explicit = is_explicit)
				else:
					return {
						'type': 'empty_response'
					}
			else:
				return {
					'type': 'error',
					'response_status': f'Spotify-{response.status}'
				}
			


async def search_spotify_album(artist: str, album: str, year: str = None):
	albums_data = []
	async with aiohttp.ClientSession() as session:
		query = f'artist:{artist} album:{album}'
		api_url = f'https://api.spotify.com/v1/search?q={query}&type=album&limit=50'
		api_headers = {'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}'}
		start_time = current_time_ms()
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				if json_response['albums']['items']:
					for item in json_response['albums']['items']:
						album_url = item['external_urls']['spotify']
						album_id = item['id']
						album_title = item['name']
						album_artists = [artist['name'] for artist in item['artists']]
						album_cover = item['images'][0]['url']
						album_year = item['release_date'][:4]
						albums_data.append({
							'type': 'album',
							'url': album_url,
							'id': album_id,
							'title': album_title,
							'artists': album_artists,
							'cover': album_cover,
							'year': album_year,
							'extra': {
								'api_time_ms': current_time_ms() - start_time,
								'response_status': f'Spotify-{response.status}'
							}
						})
					return filter_album(albums_data = albums_data, artist = artist, album = album, year = year)
				else:
					return {
						'type': 'empty_response'
					}
			else:
				return {
					'type': 'error',
					'response_status': f'Spotify-{response.status}'
				}