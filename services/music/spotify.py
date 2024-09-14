import aiohttp
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *



client_id = tokens['spotify']['id']
client_secret = tokens['spotify']['secret']


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
				error = {
					'type': 'error',
					'response_status': f'Spotify-GetAccessToken-{response.status}'
				}
				await log('ERROR - Spotify API', error['response_status'],f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal']) else tokens['discord']['logs_channel']))
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
		timeout = aiohttp.ClientTimeout(total = 30)
		async with session.get(url = api_url, headers = api_headers, timeout = timeout) as response:
			if response.status == 200:
				json_response = await response.json()
				track_url = json_response['external_urls']['spotify']
				track_id = json_response['id']
				track_title = json_response['name']
				track_artists = [artist['name'] for artist in json_response['artists']]
				track_cover = json_response['album']['images'][0]['url']
				track_collection = remove_feat(json_response['album']['name'])
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
						'response_status': f'Spotify-GetTrack-{response.status}'
					}
				}
			else:
				error = {
					'type': 'error',
					'response_status': f'Spotify-GetTrack-{response.status}'
				}
				await log('ERROR - Spotify API', error['response_status'],f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal']) else tokens['discord']['logs_channel']))
				return error



async def get_spotify_album(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.spotify.com/v1/albums/{identifier}'
		api_headers = {'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}'}
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		async with session.get(url = api_url, headers = api_headers, timeout = timeout) as response:
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
						'response_status': f'Spotify-GetAlbum-{response.status}'
					}
				}
			else:
				error = {
					'type': 'error',
					'response_status': f'Spotify-GetAlbum-{response.status}'
				}
				await log('ERROR - Spotify API', error['response_status'],f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal']) else tokens['discord']['logs_channel']))
				return error



async def search_spotify_track(artist: str, track: str, collection: str = None, is_explicit: bool = None):
	artist = artist.replace("'",'').replace(",",'')
	track = track.replace("'",'').replace(",",'')
	collection = collection.replace("'",'').replace(",",'') if collection != None else None
	artist = optimize_for_search(artist)
	track = optimize_for_search(track)
	collection = clean_up_collection_title(optimize_for_search(collection)) if collection != None else None
	tracks_data = []
	async with aiohttp.ClientSession() as session:
		query = f'artist:{artist} track:{track}'
		if collection != None:
			query = f'artist:{artist} track:{track} album:{collection}'
		api_url = f'https://api.spotify.com/v1/search?q={query}&type=track&limit=50'
		api_headers = {'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}'}
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		async with session.get(url = api_url, headers = api_headers, timeout = timeout) as response:
			if response.status == 200:
				json_response = await response.json()
				if json_response['tracks']['items']:
					for item in json_response['tracks']['items']:
						track_url = item['external_urls']['spotify']
						track_id = item['id']
						track_title = item['name']
						track_artists = [artist['name'] for artist in item['artists']]
						track_cover = item['album']['images'][0]['url']
						track_collection = remove_feat(item['album']['name'])
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
								'response_status': f'Spotify-SearchTrack-{response.status}'
							}
						})
					return filter_track(tracks_data = tracks_data, artist = artist, track = track, collection = collection, is_explicit = is_explicit)
				else:
					return {
						'type': 'empty_response'
					}
			else:
				error = {
					'type': 'error',
					'response_status': f'Spotify-SearchTrack-{response.status}'
				}
				await log('ERROR - Spotify API', error['response_status'],f'Artist: `{artist}`\nTrack: `{track}`\nCollection: `{collection}`\nIs explicit? `{is_explicit}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal']) else tokens['discord']['logs_channel']))
				return error



async def search_spotify_album(artist: str, album: str, year: str = None):
	artist = artist.replace("'",'').replace(",",'')
	album = album.replace("'",'').replace(",",'')
	artist = optimize_for_search(artist)
	album = optimize_for_search(album)
	albums_data = []
	async with aiohttp.ClientSession() as session:
		query = f'artist:{artist} album:{album}'
		api_url = f'https://api.spotify.com/v1/search?q={query}&type=album&limit=50'
		api_headers = {'Authorization': f'Bearer {await get_access_token(client_id = client_id, client_secret = client_secret)}'}
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		async with session.get(url = api_url, headers = api_headers, timeout = timeout) as response:
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
								'response_status': f'Spotify-SearchAlbum-{response.status}'
							}
						})
					return filter_album(albums_data = albums_data, artist = artist, album = album, year = year)
				else:
					return {
						'type': 'empty_response'
					}
			else:
				error = {
					'type': 'error',
					'response_status': f'Spotify-SearchAlbum-{response.status}'
				}
				await log('ERROR - Spotify API', error['response_status'],f'Artist: `{artist}`\nTrack: `{track}`Year: `{year}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal']) else tokens['discord']['logs_channel']))
				return error
