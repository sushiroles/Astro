from bandcamp_api import Bandcamp
from datetime import *
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *

bc = Bandcamp()



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

