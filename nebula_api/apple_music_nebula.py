import requests
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
	search_results = response.json()['results']

	if search_results != []:
		for result in search_results:
			url = str(result['trackViewUrl'])
			identifier = str(result['trackId'])
			artists = split_artists(str(result['artistName']))
			title = str(result['trackName'])
			year = str(result['releaseDate'][:4])
			cover = str(result['artworkUrl100'])
			tracks_data.append({
				'url': url,
				'id': identifier,
				'artists': artists,
				'track': title,
				'year': year,
				'cover': cover,
			})
		return filter_track(artist, track, tracks_data)
	else:
		return None



def search_apple_music_album(artist, album):
	albums_data = []

	url = f"https://itunes.apple.com/search?term={artist}+{album}&entity=album"
	response = requests.get(url)
	search_results = response.json()['results']

	if search_results != []:
		for result in search_results:
			url = str(result['collectionViewUrl'])
			identifier = str(result['collectionId'])
			artists = split_artists(str(result['artistName']))
			title = str(result['collectionName'])
			year = str(result['releaseDate'][:4])
			cover = str(result['artworkUrl100'])
			albums_data.append({
				'url': url,
				'id': identifier,
				'artists': artists,
				'album': title,
				'year': year,
				'cover': cover,
			})
		return filter_album(artist, album, albums_data)
	else:
		return None
