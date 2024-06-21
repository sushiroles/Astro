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
		search_results = list(set(client.search(track = track, artist = artist)))[:10]
		for result in search_results:
			tracks_data.append({
				'url': str(result.link),
				'id': str(result.id),
				'artist_name': str(result.artist.name),
				'track_name': str(result.title),
				'cover_art': str(result.album.cover_xl),
			})
		return filter_track(artist, track, tracks_data)
	except:
		return None



def search_deezer_album(artist: str, album: str):
	try:
		albums_data = []
		search_results = client.search_albums(query=f'{artist} {album}')[:10]
		for result in search_results:
			albums_data.append({
				'url': str(result.link),
				'id': str(result.id),
				'artist_name': str(result.artist.name),
				'album_name': str(result.title),
				'release_year': str(result.release_date.strftime('%Y')),
				'cover_art': str(result.cover_xl),
			})
		return filter_album(artist, album, albums_data)
	except:
		return None
