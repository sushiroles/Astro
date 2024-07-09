import requests
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *



def is_apple_music_track(url: str):
	if url.find('https://music.apple.com/') >= 0 and url.find('?i=') >= 0:
		return True
	else:
		return False

def is_apple_music_album(url: str):
	if url.find('https://music.apple.com/') >= 0 and not url.find('?i=') >= 0:
		return True
	else:
		return False
	
def get_apple_music_track_id(url: str):
	index = url.index('?i=') + 3
	return url[index:]

def get_apple_music_album_id(url: str):
	index = len(url) - 1
	while url[index] != '/':
		index -= 1
	return url[index+1:]

	
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



def get_apple_music_track(identifier: str):
	track_data = []

	url = f"https://itunes.apple.com/lookup?id={identifier}"
	response = requests.get(url)
	result = response.json()['results'][0]

	if result != []:
		url = str(result['trackViewUrl'])
		identifier = str(result['trackId'])
		artists = split_artists(str(result['artistName']))
		title = str(result['trackName'])
		year = str(result['releaseDate'][:4])
		cover = str(result['artworkUrl100'])
		track_data.append({
			'url': url,
			'id': identifier,
			'artists': artists,
			'track': title,
			'year': year,
			'cover': cover,
		})
		return track_data[0]
	else:
		return None



def get_apple_music_album(identifier: str):
	object_data = []

	url = f"https://itunes.apple.com/lookup?id={identifier}"
	response = requests.get(url)
	result = response.json()['results'][0]

	if result != []:
		url = str(result['collectionViewUrl'])
		identifier = str(result['collectionId'])
		artists = split_artists(str(result['artistName']))
		title = str(result['collectionName'])
		year = str(result['releaseDate'][:4])
		cover = str(result['artworkUrl100'])
		object_data.append({
			'url': url,
			'id': identifier,
			'artists': artists,
			'album': title,
			'year': year,
			'cover': cover,
		})
		return object_data[0]
	else:
		return None
