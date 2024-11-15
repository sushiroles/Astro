import aiohttp
import asyncio
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *



def is_apple_music_track(url: str):
	return bool(url.find('https://music.apple.com/') >= 0 and url.find('/song/') >= 0 or url.find('https://music.apple.com/') >= 0 and url.find('/album/') >= 0 and url.find('?i=') >= 0)

def is_apple_music_album(url: str):
	return bool(url.find('https://music.apple.com/') >= 0 and url.find('/album/') >=0 and not url.find('?i=') >= 0)

def is_apple_music_video(url: str):
	return bool(url.find('https://music.apple.com/') >= 0 and url.find('/music-video/') >=0)

def get_apple_music_track_id(url: str):
	if url.find('/song/') >= 0:
		index = len(url) - 1
		while url[index] != '/':
			index -= 1
		return {
			'id': url[index+1:],
			'country_code': url[24:26],
		}
	else:
		if url.find('&uo=') >= 0:
			return {
				'id': url[url.index('?i=')+3:url.index('&uo=')],
				'country_code': url[24:26],
			}
		else:
			return {
				'id': url[url.index('?i=')+3:],
				'country_code': url[24:26],
			}

def get_apple_music_album_video_id(url: str):
	index = len(url) - 1
	while url[index] != '/':
		index -= 1
	if '?uo' in url:
		return {
			'id': url[index+1:url.index('?uo')],
			'country_code': url[24:26],
		}
	else:
		return {
			'id': url[index+1:],
			'country_code': url[24:26],
		}

async def get_apple_music_artist(artist_id: int, country_code: str):
	async with aiohttp.ClientSession() as session:
		api_url = f"https://itunes.apple.com/lookup"
		api_params = {
			'id': artist_id,
			'country': country_code
		}
		timeout = aiohttp.ClientTimeout(total = 30)
		while True:
			async with session.get(url = api_url, timeout = timeout, params = api_params) as response:
				if response.status == 200:
					json_response = await response.json(content_type = 'text/javascript')
					result = json_response['results'][0]
					return [result['artistName']]
				elif response.status == 503:
					await asyncio.sleep(0.1)
					continue
				else:
					error = {
						'type': 'error',
						'response_status': f'AppleMusic-GetArtist-{response.status}'
					}
					await log('ERROR - Apple Music API', error['response_status'],f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
					return []



async def get_apple_music_track(identifier: str, country_code: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://itunes.apple.com/lookup'
		api_params = {
			'id': identifier,
			'country': country_code
		}
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		while True:
			async with session.get(url = api_url, timeout = timeout, params = api_params) as response:
				if response.status == 200:
					json_response = await response.json(content_type = 'text/javascript')
					result = json_response['results'][0]
					track_url = result['trackViewUrl']
					track_id = str(result['trackId'])
					track_title = result['trackName']
					track_artists = await get_apple_music_artist(result['artistId'], country_code = country_code)
					track_cover = result['artworkUrl100']
					track_collection = remove_feat(result['collectionName']) if 'song' in result['kind'] else None
					track_is_explicit = not 'not' in result['trackExplicitness']
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
							'response_status': f'AppleMusic-GetTrack-{response.status}'
						}
					}
				elif response.status == 503:
					await asyncio.sleep(0.1)
					continue
				else:
					error = {
						'type': 'error',
						'response_status': f'AppleMusic-GetTrack-{response.status}'
					}
					await log('ERROR - Apple Music API', error['response_status'],f'ID: `{identifier}`\nCountry code: `{country_code}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
					return error



async def get_apple_music_album(identifier: str, country_code: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://itunes.apple.com/lookup'
		api_params = {
			'id': identifier,
			'country': country_code
		}
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		while True:
			async with session.get(url = api_url, timeout = timeout, params = api_params) as response:
				if response.status == 200:
					json_response = await response.json(content_type = 'text/javascript')
					result = json_response['results'][0]
					album_url = result['collectionViewUrl']
					album_id = str(result['collectionId'])
					album_title = result['collectionName']
					album_artists = await get_apple_music_artist(result['artistId'], country_code = country_code)
					album_cover = result['artworkUrl100']
					album_year = result['releaseDate'][:4]
					if ' - Single' in album_title:
						track_is_explicit = not 'not' in result['collectionExplicitness']
						return {
							'type': 'track',
							'url': album_url,
							'id': album_id,
							'title': album_title.replace(' - Single',''),
							'artists': album_artists,
							'cover': album_cover,
							'collection_name': remove_feat(album_title),
							'is_explicit': track_is_explicit,
							'extra': {
								'api_time_ms': current_time_ms() - start_time,
								'response_status': f'AppleMusic-GetAlbum-{response.status}'
							}
						}
					if ' (Apple Music Edition)' in album_title:
						album_title = album_title.replace(' (Apple Music Edition)', '')
					if ' - EP' in album_title:
						album_title = album_title.replace(' - EP', '')
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
							'response_status': f'AppleMusic-GetAlbum-{response.status}'
						}
					}
				elif response.status == 503:
					await asyncio.sleep(0.1)
					continue
				else:
					error = {
						'type': 'error',
						'response_status': f'AppleMusic-GetAlbum-{response.status}'
					}
					await log('ERROR - Apple Music API', error['response_status'],f'ID: `{identifier}`\nCountry code: `{country_code}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
					return error



async def search_apple_music_track(artist: str, track: str, collection: str = None, is_explicit: bool = None):
	track = replace_with_ascii(track).lower()
	artist = optimize_for_search(artist).lower()
	track = optimize_for_search(track).lower()
	collection = optimize_for_search(collection).lower() if collection != None else None
	tracks_data = []
	async with aiohttp.ClientSession() as session:
		api_url = f'https://itunes.apple.com/search'
		api_params = {
			'term': (f'{artist} "{track}"' if collection == None else f'{artist} "{track}" {collection}'),
			'entity': 'song',
			'limit': '200',
			'country': 'us'
		}
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		while True:
			async with session.get(url = api_url, timeout = timeout, params = api_params) as response:
				if response.status == 200:
					json_response = await response.json(content_type = 'text/javascript')
					search_results = json_response['results']
					if search_results != []:
						for item in search_results:
							track_url = item['trackViewUrl']
							track_id = str(item['trackId'])
							track_title = item['trackName']
							track_artists = split_artists(item['artistName'])
							track_cover = item['artworkUrl100']
							track_collection = remove_feat(clean_up_collection_title(item['collectionName']))
							track_is_explicit = not 'not' in item['trackExplicitness']
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
									'response_status': f'AppleMusic-SearchTrack-{response.status}'
								}
							})
						return filter_track(tracks_data = tracks_data, artist = artist, track = track, collection = collection, is_explicit = is_explicit)
					else:
						return {
							'type': 'empty_response'
						}
				elif response.status == 503:
					await asyncio.sleep(0.1)
					continue
				else:
					error = {
						'type': 'error',
						'response_status': f'AppleMusic-SearchTrack-{response.status}'
					}
					await log('ERROR - Apple Music API', error['response_status'],f'Artist: `{artist}`\nTrack: `{track}`\nCollection: `{collection}`\nIs explicit? `{is_explicit}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
					return error



async def search_apple_music_album(artist: str, album: str, year: str = None):
	album = replace_with_ascii(album)
	artist = optimize_for_search(artist)
	album = optimize_for_search(album)
	albums_data = []
	async with aiohttp.ClientSession() as session:
		query = f'{artist} "{album}"'
		api_url =f'https://itunes.apple.com/search'
		api_params = {
			'term': query,
			'entity': 'album',
			'limit': '200',
			'country': 'us'
		}
		timeout = aiohttp.ClientTimeout(total = 30)
		start_time = current_time_ms()
		while True:
			async with session.get(url = api_url, timeout = timeout, params = api_params) as response:
				if response.status == 200:
					json_response = await response.json(content_type = 'text/javascript')
					search_results = json_response['results']
					if search_results != []:
						for item in search_results:
							album_url = item['collectionViewUrl']
							album_id = str(item['collectionId'])
							album_title = item['collectionName']
							album_artists = split_artists(item['artistName'])
							album_cover = item['artworkUrl100']
							album_year = item['releaseDate'][:4]
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
									'response_status': f'AppleMusic-SearchAlbum-{response.status}'
								}
							})
						return filter_album(albums_data = albums_data, artist = artist, album = album, year = year)
					else:
						return {
							'type': 'empty_response'
						}
				elif response.status == 503:
					await asyncio.sleep(0.1)
					continue
				else:
					error = {
						'type': 'error',
						'response_status': f'AppleMusic-SearchAlbum-{response.status}'
					}
					await log('ERROR - Apple Music API', error['response_status'],f'Artist: `{artist}`\nTrack: `{track}`Year: `{year}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
					return error
