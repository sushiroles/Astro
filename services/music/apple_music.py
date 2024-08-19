import aiohttp
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

async def get_apple_music_artist(artist_id: int):
	async with aiohttp.ClientSession() as session:
		api_url = f"https://itunes.apple.com/lookup?id={artist_id}"
		while True:
			async with session.get(url = api_url) as response:
				if response.status == 200:
					json_response = await response.json(content_type = None)
					result = json_response['results'][0]
					return [result['artistName']]
				if response.status == 503:
					continue
				else:
					return []



async def get_apple_music_track(identifier: str, country_code: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://itunes.apple.com/lookup?id={identifier}&country={country_code}'
		while True:
			async with session.get(url = api_url) as response:
				if response.status == 200:
					json_response = await response.json(content_type = None)
					result = json_response['results'][0]
					track_url = result['trackViewUrl']
					track_id = str(result['trackId'])
					track_title = result['trackName']
					track_artists = await get_apple_music_artist(result['artistId'])
					track_cover = result['artworkUrl100']
					return {
						'url': track_url,
						'id': track_id,
						'track': track_title,
						'artists': track_artists,
						'cover': track_cover,
					}
				elif response.status == 503:
					continue
				else:
					return None



async def get_apple_music_album(identifier: str, country_code: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://itunes.apple.com/lookup?id={identifier}&country={country_code}'
		while True:
			async with session.get(url = api_url) as response:
				if response.status == 200:
					json_response = await response.json(content_type = None)
					result = json_response['results'][0]
					album_url = result['collectionViewUrl']
					album_id = str(result['collectionId'])
					album_title = result['collectionName']
					album_artists = await get_apple_music_artist(result['artistId'])
					album_cover = result['artworkUrl100']
					if ' - Single' in album_title:
						return {
							'url': album_url,
							'id': album_id,
							'track': album_title.replace(' - Single',''),
							'artists': album_artists,
							'cover': album_cover,
						}
					if ' (Apple Music Edition)' in album_title:
						album_title = album_title.replace(' (Apple Music Edition)', '')
					if ' - EP' in album_title:
						album_title = album_title.replace(' - EP', '')
					return {
						'url': album_url,
						'id': album_id,
						'album': album_title,
						'artists': album_artists,
						'cover': album_cover,
					}
				elif response.status == 503:
					continue
				else:
					return None



async def search_apple_music_track(artist: str, track: str):
	tracks_data = []
	async with aiohttp.ClientSession() as session:
		query = f'{artist}+{track}'
		api_url =f'https://itunes.apple.com/search?term={query}&entity=song&limit=200&country=us'
		while True:
			async with session.get(url = api_url) as response:
				if response.status == 200:
					json_response = await response.json(content_type = None)
					search_results = json_response['results']
					if search_results != []:
						for item in search_results:
							track_url = item['trackViewUrl']
							track_id = str(item['trackId'])
							track_title = item['trackName']
							track_artists = split_artists(item['artistName'])
							track_cover = item['artworkUrl100']
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
				elif response.status == 503:
					continue
				else:
					return None
			


async def search_apple_music_album(artist: str, album: str):
	albums_data = []
	async with aiohttp.ClientSession() as session:
		query = f'{artist}+{album}'
		api_url =f'https://itunes.apple.com/search?term={query}&entity=album&limit=200&country=us'
		while True:
			async with session.get(url = api_url) as response:
				if response.status == 200:
					json_response = await response.json(content_type = None)
					search_results = json_response['results']
					if search_results != []:
						for item in search_results:
							album_url = item['collectionViewUrl']
							album_id = str(item['collectionId'])
							album_title = item['collectionName']
							album_artists = split_artists(item['artistName'])
							album_cover = item['artworkUrl100']
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
				elif response.status == 503:
					continue
				else:
					return None
