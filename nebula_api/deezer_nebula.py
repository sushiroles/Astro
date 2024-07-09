import requests
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *
from datetime import *



def get_object_year(object_id: str, object_type: str):
	url = f'https://api.deezer.com/{object_type}/{object_id}'
	response = requests.get(url)
	result = response.json()
	release_year = result['release_date'][:4]
	return release_year


def search_deezer_track(artist: str, track: str):
	tracks_data = []
	url = f'https://api.deezer.com/search/track?q={artist}-{track}'
	response = requests.get(url)
	search_results = response.json()['data']

	if search_results != []:
		for result in search_results:
			if str(result['type']) == 'track':
				url = str(result['link'])
				identifier = str(result['id'])
				artists = [str(result['artist'])]
				title = str(result['title'])
				year = ''
				cover = str(result['album']['cover_xl'])
				tracks_data.append({
					'url': url,
					'id': identifier,
					'artists': artists,
					'track': title,
					'year': year,
					'cover': cover,
				})
		try:
			filtered_track = filter_track(artist, track, tracks_data)
			filtered_track['year'] = get_object_year(filtered_track['id'],'track')
		except:
			return None
		return filter_track(artist, track, tracks_data)
	else:
		return None



def search_deezer_album(artist: str, album: str):
	tracks_data = []
	url = f'https://api.deezer.com/search/album?q={artist}-{album}'
	response = requests.get(url)
	search_results = response.json()['data']

	if search_results != []:
		for result in search_results:
			if str(result['type']) == 'album':
				url = str(result['link'])
				identifier = str(result['id'])
				artists = [str(result['artist'])]
				title = str(result['title'])
				year = ''
				cover = str(result['cover_xl'])
				tracks_data.append({
					'url': url,
					'id': identifier,
					'artists': artists,
					'album': title,
					'year': year,
					'cover': cover,
				})
		try:
			filtered_album = filter_album(artist, album, tracks_data)
			filtered_album['year'] = get_object_year(filtered_album['id'],'album')
		except:
			return None
		return filtered_album
	else:
		return None
