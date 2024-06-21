import requests
import json
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *



def search_apple_music_track(artist, track):
	tracks_data = []

	url = f"https://itunes.apple.com/search?term={artist}+{track}&entity=song"
	response = requests.get(url)
	search_results = response.json()['results'][:10]

	if search_results != []:
		for result in search_results:
			tracks_data.append({
				'url': str(result['trackViewUrl']),
				'id': str(result['trackId']),
				'artist_name': str(result['artistName']),
				'track_name': str(result['trackName']),
				'cover_art': str(result['artworkUrl100']),
			})
		return filter_track(artist, track, tracks_data)
	else:
		return None



def search_apple_music_album(artist, album):
	albums_data = []

	url = f"https://itunes.apple.com/search?term={artist}+{album}&entity=album"
	response = requests.get(url)
	search_results = response.json()['results'][:10]

	if search_results != []:
		for result in search_results:
			albums_data.append({
				'url': str(result['collectionViewUrl']),
				'id': str(result['collectionId']),
				'artist_name': str(result['artistName']),
				'album_name': str(result['collectionName']),
				'release_year': str(result['releaseDate'][:4]),
				'cover_art': str(result['artworkUrl100']),
			})
		return filter_album(artist, album, albums_data)
	else:
		return None
