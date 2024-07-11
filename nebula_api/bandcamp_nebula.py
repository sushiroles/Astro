from bandcamp_api import Bandcamp
from datetime import *
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *



bc = Bandcamp()



def is_bandcamp_track(url: str):
	return bool(url.find('bandcamp.com/track/') >= 0)

def is_bandcamp_album(url: str):
	return bool(url.find('bandcamp.com/album/') >= 0)



def search_bandcamp_track(artist: str, track: str):
	try:
		tracks_data = []
		search_results = bc.search(f'{artist} {track}')
		for result in search_results:
			if result.type == 'track':
				url = str(result.track_url)
				identifier = str(result.track_id)
				artists = split_artists(str(result.artist_title))
				title = str(result.track_title)
				year = '' # fuck you
				cover = str(result.image_url)
				tracks_data.append({
					'url': url,
					'id': identifier,
					'artists': artists,
					'track': title,
					'year': year,
					'cover': cover,
				})
		return filter_track(artist, track, tracks_data)
	except:
		return None



def search_bandcamp_album(artist: str, album: str):
	try:
		albums_data = []
		search_results = bc.search(f'{artist} {album}')
		for result in search_results:
			if result.type == 'album':
				url = str(result.album_url)
				identifier = str(result.album_id)
				artists = split_artists(str(result.artist_title))
				title = str(result.album_title)
				year = '' # fuck you
				cover = str(result.image_url)
				albums_data.append({
					'url': url,
					'id': identifier,
					'artists': artists,
					'album': title,
					'year': year, 
					'cover': cover,
				})
		return filter_album(artist, album, albums_data)
	except:
		return None



def get_bandcamp_track_parameters(url: str):
	artist = url[url.index("://")+3:url.index('.bandcamp.com')].replace('-',' ')
	track = url[url.index('track/')+6:].replace('-',' ')
		
	return {
		'artists': [artist],
		'track': track,
	}



def get_bandcamp_album_parameters(url: str):
	artist = url[url.index("://")+3:url.index('.bandcamp.com')].replace('-',' ')
	album = url[url.index('album/')+6:].replace('-',' ')

	return {
		'artists': [artist],
		'album': album,
	}

