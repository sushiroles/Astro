import deezer
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *
from datetime import *

client = deezer.Client()



def search_deezer_track(artist: str, track: str):
	try:
		tracks_data = []
		search_results = client.search(track = track, artist = artist)
		for result in search_results:
			url = str(result.link)
			identifier = str(result.id)
			artists = [str(result.artist.name)]
			title = str(result.title)
			year = str(result.release_date.strftime('%Y'))
			cover = str(result.album.cover_xl)
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



def search_deezer_album(artist: str, album: str):
	try:
		albums_data = []
		search_results = client.search_albums(query = f'{artist} {album}')
		for result in search_results:
			url = str(result.link)
			identifier = str(result.id)
			artists = [str(result.artist.name)]
			title = str(result.title)
			year = str(result.release_date.strftime('%Y'))
			cover = str(result.cover_xl)
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
