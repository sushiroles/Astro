import deezer

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
	except:
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
	except:
		return None
