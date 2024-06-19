import deezer
from etc import *

client = deezer.Client()

def search_deezer_track(artist: str, track: str):
	try:
		tracks_data = []
		search_results = list(set(client.search(track = track, artist = artist)))[:5]
		for search_results_num in range(len(search_results)):
			tracks_data.append({
				'url': search_results[search_results_num].link,
				'id': search_results[search_results_num].id,
				'artist_name': search_results[search_results_num].artist.name,
				'track_name': search_results[search_results_num].title,
				'cover_art': search_results[search_results_num].album.cover_xl,
			})
		return tracks_data
	except:
		return None

def search_deezer_album(artist: str, album: str):
	try:
		albums_data = []
		search_results = list(set(client.search(album = album, artist = artist)))[:5]
		for search_results_num in range(len(search_results)):
			albums_data.append({
				'url': search_results[search_results_num].album.link,
				'id': search_results[search_results_num].album.id,
				'artist_name': search_results[search_results_num].artist.name,
				'album_name': search_results[search_results_num].album.title,
				'cover_art': search_results[search_results_num].album.cover_xl,
			})
		return albums_data
	except:
		return None
