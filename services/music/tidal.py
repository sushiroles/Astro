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
	return bool(url.find('https://tidal.com/') >= 0 and url.find('/track/') >= 0)

def is_tidal_album(url: str):
	return bool(url.find('https://tidal.com/') >= 0 and url.find('/album/') >= 0)

def is_tidal_video(url: str):
	return bool(url.find('https://tidal.com/') >= 0 and url.find('/video/') >= 0)

def get_tidal_track_id(url: str):
	if '?u' in url:
		return str(url[url.index('/track/') + 7:url.index('?u')])
	else:
		return str(url[url.index('/track/') + 7:])

def get_tidal_album_id(url: str):
	if '?u' in url:
		return str(url[url.index('/album/') + 7:url.index('?u')])
	else:
		return str(url[url.index('/album/') + 7:])
	
def get_tidal_video_id(url: str):
	if '?u' in url:
		return str(url[url.index('/video/') + 7:url.index('?u')])
	else:
		return str(url[url.index('/video/') + 7:])


async def get_tidal_track(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://openapi.tidal.com/tracks/{identifier}?countryCode=US'
		api_headers = {
			'accept': 'application/vnd.api+json',
			'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}',
			'Content-Type': 'application/vnd.tidal.v1+json'
		}
		start_time = current_time_ms()
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				track_url = json_response['resource']['tidalUrl']
				track_id = json_response['resource']['id']
				track_title = json_response['resource']['title']
				track_artists = [artist['name'] for artist in json_response['resource']['artists']]
				track_cover = json_response['resource']['album']['imageCover'][1]['url']
				return {
					'type': 'track',
					'url': track_url,
					'id': track_id,
					'title': track_title,
					'artists': track_artists,
					'cover': track_cover,
					'extra': {
						'api_time_ms': current_time_ms() - start_time,
						'response_status': f'TIDAL-{response.status}'
					}
				}
			else:
				return {
					'type': 'error',
					'response_status': f'TIDAL-{response.status}'
				}
			


async def get_tidal_album(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://openapi.tidal.com/albums/{identifier}?countryCode=US'
		api_headers = {
			'accept': 'application/vnd.api+json',
			'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}',
			'Content-Type': 'application/vnd.tidal.v1+json'
		}
		start_time = current_time_ms()
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				album_url = json_response['resource']['tidalUrl']
				album_id = json_response['resource']['id']
				album_title = json_response['resource']['title']
				album_artists = [artist['name'] for artist in json_response['resource']['artists']]
				album_cover = json_response['resource']['imageCover'][1]['url']
				album_year = json_response['resource']['releaseDate'][:4]
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
						'response_status': f'TIDAL-{response.status}'
					}
				}
			else:
				return {
					'type': 'error',
					'response_status': f'TIDAL-{response.status}'
				}



async def get_tidal_video(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://openapi.tidal.com/videos/{identifier}?countryCode=US'
		api_headers = {
			'accept': 'application/vnd.api+json',
			'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}',
			'Content-Type': 'application/vnd.tidal.v1+json'
		}
		start_time = current_time_ms()
		async with session.get(url = api_url, headers = api_headers) as response:
			if response.status == 200:
				json_response = await response.json()
				video_url = json_response['resource']['tidalUrl']
				video_id = json_response['resource']['id']
				video_title = json_response['resource']['title']
				video_artists = [artist['name'] for artist in json_response['resource']['artists']]
				video_cover = json_response['resource']['image'][1]['url']
				return {
					'type': 'track',
					'url': video_url,
					'id': video_id,
					'title': video_title,
					'artists': video_artists,
					'cover': video_cover,
					'extra': {
						'api_time_ms': current_time_ms() - start_time,
						'response_status': f'TIDAL-{response.status}'
					}
				}
			else:
				return {
					'type': 'error',
					'response_status': f'TIDAL-{response.status}'
				}



async def search_tidal_track(artist: str, track: str):
	tracks_data = []
	async with aiohttp.ClientSession() as session:
		query = f'{track} {artist}'
		api_url = f"https://openapi.tidal.com/search?query={query}&type=TRACKS&offset=0&limit=100&countryCode=US&popularity=WORLDWIDE"
		api_headers = {
			'accept': 'application/vnd.api+json',
			'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}',
			'Content-Type': 'application/vnd.tidal.v1+json'
		}
		start_time = current_time_ms()
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
							'type': 'track',
							'url': track_url,
							'id': track_id,
							'title': track_title,
							'artists': track_artists,
							'cover': track_cover,
							'extra': {
								'api_time_ms': current_time_ms() - start_time,
								'response_status': f'TIDAL-{response.status}'
							}
						})
					return filter_track(artist = artist, track = track, tracks_data = tracks_data)
				else:
					return {
						'type': 'empty_response'
					}
			else:
				return {
					'type': 'error',
					'response_status': f'TIDAL-{response.status}'
				}



async def search_tidal_album(artist: str, album: str):
	albums_data = []
	async with aiohttp.ClientSession() as session:
		query = f'{artist} {album}'
		api_url = f"https://openapi.tidal.com/search?query={query}&type=ALBUMS&offset=0&limit=100&countryCode=US&popularity=WORLDWIDE"
		api_headers = {
			'accept': 'application/vnd.api+json',
			'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}',
			'Content-Type': 'application/vnd.tidal.v1+json'
		}
		start_time = current_time_ms()
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
						album_year = item['resource']['releaseDate'][:4]
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
								'response_status': f'TIDAL-{response.status}'
							}
						})
					return filter_album(artist = artist, album = album, albums_data = albums_data)
				else:
					return {
						'type': 'empty_response'
					}
			else:
				return {
					'type': 'error',
					'response_status': f'TIDAL-{response.status}'
				}
