import aiohttp
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *



def is_deferred_url(url: str):
	return bool(url.find('https://deezer.page.link/') >= 0)

def is_deezer_track(url: str):
	if is_deferred_url(url):
		url = get_regular_url(url)
	return bool(url.find('https://www.deezer.com') >= 0 and url.find('track') >= 0)

def is_deezer_album(url: str):
	if is_deferred_url(url):
		url = get_regular_url(url)
	return bool(url.find('https://www.deezer.com') >= 0 and url.find('album') >= 0)

def get_deezer_track_id(url: str):
	if is_deferred_url(url):
		url = get_regular_url(url)
	if url.find('?') >= 0:
		return str(url[url.index('track/')+6:url.index('?')])
	else:
		return str(url[url.index('track/')+6:])

def get_deezer_album_id(url: str):
	if is_deferred_url(url):
		url = get_regular_url(url)
	if url.find('?') >= 0:
		return str(url[url.index('album/')+6:url.index('?')])
	else:
		return str(url[url.index('album/')+6:])



async def get_deezer_track(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.deezer.com/track/{identifier}'
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		async with session.get(url = api_url, timeout = timeout) as response:
			if response.status == 200:
				json_response = await response.json()
				track_url = json_response['link']
				track_id = str(json_response['id'])
				track_title = json_response['title']
				track_artists = [artist['name'] for artist in json_response['contributors']]
				track_cover = json_response['album']['cover_xl']
				track_collection = remove_feat(json_response['album']['title'])
				track_is_explicit = json_response['explicit_lyrics']
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
						'api_time_ms': current_time_ms() - start_time,
						'response_status': f'Deezer-GetTrack-{response.status}'
					}
				}
			else:
				error = {
					'type': 'error',
					'response_status': f'Deezer-GetTrack-{response.status}'
				}
				await log('ERROR - Deezer API', error['response_status'],f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
				return error



async def get_deezer_album(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.deezer.com/album/{identifier}'
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		async with session.get(url = api_url, timeout = timeout) as response:
			if response.status == 200:
				json_response = await response.json()
				album_url = json_response['link']
				album_id = str(json_response['id'])
				album_title = json_response['title']
				album_artists = [artist['name'] for artist in json_response['contributors']]
				album_cover = json_response['cover_xl']
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
						'response_status': f'Deezer-GetAlbum-{response.status}'
					}
				}
			else:
				error = {
					'type': 'error',
					'response_status': f'Deezer-GetTrack-{response.status}'
				}
				await log('ERROR - Deezer API', error['response_status'],f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
				return error



async def search_deezer_track(artist: str, track: str, collection: str = None, is_explicit: bool = None):
	artist = optimize_for_search(artist)
	track = optimize_for_search(track)
	collection = clean_up_collection_title(optimize_for_search(collection)) if collection != None else None
	tracks_data = []
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.deezer.com/search/track'
		api_params = {
			'q': (f'artist:"{artist}" track:"{track}"' if collection == None else f'artist:"{artist}" track:"{track}" album:"{collection}"'),
		}
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		async with session.get(url = api_url, timeout = timeout, params = api_params) as response:
			if response.status == 200:
				json_response = await response.json()
				search_results = json_response['data']
				if search_results != []:
					for item in search_results:
						async with session.get(url = f'https://api.deezer.com/track/{item['id']}') as result:
							data = await result.json()
							track_url = data['link']
							track_id = str(data['id'])
							track_title = data['title']
							track_artists = [artist['name'] for artist in data['contributors']]
							track_cover = data['album']['cover_xl']
							track_collection = remove_feat(data['album']['title'])
							track_is_explicit = data['explicit_lyrics']
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
									'response_status': f'Deezer-SearchTrack-{response.status}'
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
					'response_status': f'Deezer-SearchTrack-{response.status}'
				}
				await log('ERROR - Deezer API', error['response_status'],f'Artist: `{artist}`\nTrack: `{track}`\nCollection: `{collection}`\nIs explicit? `{is_explicit}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
				return error



async def search_deezer_album(artist: str, album: str, year: str = None):
	artist = optimize_for_search(artist)
	album = optimize_for_search(album)
	albums_data = []
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.deezer.com/search/album'
		api_params = {
			'q': f'artist:"{artist}" album:"{album}"',
		}
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		async with session.get(url = api_url, timeout = timeout, params = api_params) as response:
			if response.status == 200:
				json_response = await response.json()
				search_results = json_response['data']
				if search_results != []:
					for item in search_results:
						async with session.get(url = f'https://api.deezer.com/album/{item['id']}') as result:
							data = await result.json()
							album_url = data['link']
							album_id = str(data['id'])
							album_title = data['title']
							album_artists = [artist['name'] for artist in data['contributors']]
							album_cover = data['cover_xl']
							album_year = data['release_date'][:4]
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
									'response_status': f'Deezer-SearchAlbum-{response.status}'
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
					'response_status': f'Deezer-SearchAlbum-{response.status}'
				}
				await log('ERROR - Deezer API', error['response_status'],f'Artist: `{artist}`\nTrack: `{track}`Year: `{year}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
				return error
