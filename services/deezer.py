import requests
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *
from datetime import *



def is_deferred_url(url: str):
	return bool(url.find('https://deezer.page.link') >= 0)

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




def search_deezer_track(artist: str, track: str):
	try:
		tracks_data = []
		url = f'https://api.deezer.com/search/track?q=artist:"{str(artist)}" track:"{str(track)}"'
		response = requests.get(url)
		search_results = response.json()['data']

		if search_results != []:
			for data in search_results:
				result = requests.get(f'https://api.deezer.com/track/{data['id']}').json()
				url = str(result['link'])
				identifier = str(result['id'])
				artists = []
				for names in result['contributors']:
					artists.append(str(names['name']))
				title = str(result['title'])
				cover = str(result['album']['cover_xl'])
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
	except:
		return None



def search_deezer_album(artist: str, album: str):
	try:
		tracks_data = []
		url = f'https://api.deezer.com/search/album?q=artist:"{str(artist)}" album:"{str(album)}"'
		response = requests.get(url)
		search_results = response.json()['data']

		if search_results != []:
			for data in search_results:
				result = requests.get(f'https://api.deezer.com/album/{data['id']}').json()
				url = str(result['link'])
				identifier = str(result['id'])
				artists = []
				for names in result['contributors']:
					artists.append(str(names['name']))
				title = str(result['title'])
				year = str(result['release_date'][:4])
				cover = str(result['cover_xl'])
				tracks_data.append({
					'url': url,
					'id': identifier,
					'artists': artists,
					'album': title,
					'cover': cover,
				})
			return filter_album(artist, album, tracks_data)
		else:
			return None
	except:
		return None



def get_deezer_track(identifier: str):
	try:
		url = f'https://api.deezer.com/track/{identifier}'
		response = requests.get(url)
		result = response.json()

		if 'error' not in result.keys():
			url = str(result['link'])
			identifier = str(result['id'])
			artists = []
			for names in result['contributors']:
				artists.append(str(names['name']))
			title = str(result['title'])
			year = str(result['release_date'][:4])
			cover = str(result['album']['cover_xl'])
			return {
				'url': url,
				'id': identifier,
				'artists': artists,
				'track': title,
				'year': year,
				'cover': cover,
			}
		else:
			return None
	except:
		return None



def get_deezer_album(identifier: str):
	try:
		url = f'https://api.deezer.com/album/{identifier}'
		response = requests.get(url)
		result = response.json()

		if 'error' not in result.keys():
			url = str(result['link'])
			identifier = str(result['id'])
			artists = []
			for names in result['contributors']:
				artists.append(str(names['name']))
			title = str(result['title'])
			year = str(result['release_date'][:4])
			cover = str(result['cover_xl'])
			return {
				'url': url,
				'id': identifier,
				'artists': artists,
				'album': title,
				'year': year,
				'cover': cover,
			}
		else:
			return None
	except:
		return None
