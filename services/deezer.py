import aiohttp
import asyncio
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
		async with session.get(url = api_url) as response:
			if response.status == 200:
				json_response = await response.json()
				track_url = json_response['link']
				track_id = str(json_response['id'])
				track_title = json_response['title']
				track_artists = [artist['name'] for artist in json_response['contributors']]
				track_cover = json_response['album']['cover_xl']
				return {
					'url': track_url,
					'id': track_id,
					'track': track_title,
					'artists': track_artists,
					'cover': track_cover,
				}
			else:
				return None



async def get_deezer_album(identifier: str):
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.deezer.com/album/{identifier}'
		async with session.get(url = api_url) as response:
			if response.status == 200:
				json_response = await response.json()
				album_url = json_response['link']
				album_id = str(json_response['id'])
				album_title = json_response['title']
				album_artists = [artist['name'] for artist in json_response['contributors']]
				album_cover = json_response['cover_xl']
				return {
					'url': album_url,
					'id': album_id,
					'album': album_title,
					'artists': album_artists,
					'cover': album_cover,
				}
			else:
				return None

			

async def search_deezer_track(artist: str, track: str):
	tracks_data = []
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.deezer.com/search/track?q=artist:"{artist}" track:"{track}"'
		async with session.get(url = api_url) as response:
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



async def search_deezer_album(artist: str, album: str):
	albums_data = []
	async with aiohttp.ClientSession() as session:
		api_url = f'https://api.deezer.com/search/album?q=artist:"{artist}" album:"{album}"'
		async with session.get(url = api_url) as response:
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
					