import deezer
from log import *

client = deezer.Client()

def search_deezer_track(artist: str, track: str):
	try:
		search = client.search(track = track, artist = artist)[0]
		return {
			'url': search.link,
			'id': search.id,
			'artist_name': search.artist.name,
			'track_name': search.title,
			'cover_art': search.album.cover_xl,
		}
	except Exception as error:
		log('ERROR', f'Inside search_deezer_track(): "{error}" --- artist: {artist} / track: {track}')
		return None

def search_deezer_album(artist: str, album: str):
	try:
		search = client.search(album = album, artist = artist)[0]
		return {
			'url': search.album.link,
			'id': search.album.id,
			'artist_name': search.artist.name,
			'album_name': search.album.title,
			'cover_art': search.album.cover_xl,
		}
	except Exception as error:
		log('ERROR', f'Inside search_deezer_album(): "{error}" --- artist: {artist} / album: {album}')
		return None

def get_deezer_track(identifier: str):
	search = client.get_track(int(identifier))
	return {
		'url': search.link,
		'id': search.id,
		'artist_name': search.artist.name,
		'track_name': search.title,
		'cover_art': search.album.cover_xl,
	}

def get_deezer_album(identifier: str):
	search = client.get_album(int(identifier))
	return {
		'url': search.album.link,
		'id': search.album.id,
		'artist_name': search.artist.name,
		'album_name': search.album.title,
		'cover_art': search.album.cover_xl,
	}