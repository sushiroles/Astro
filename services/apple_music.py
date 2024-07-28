import requests
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *



def is_apple_music_track(url: str):
	return bool(url.find('https://music.apple.com/') >= 0 and url.find('/song/') >= 0 or url.find('/album/') >= 0 and url.find('?i=') >= 0)

def is_apple_music_album(url: str):
	return bool(url.find('https://music.apple.com/') >= 0 and url.find('/album/') >=0 and not url.find('?i=') >= 0)

def get_apple_music_track_id(url: str):
	if url.find('/song/') >= 0:
		index = len(url) - 1
		while url[index] != '/':
			index -= 1
		return {
			'id': url[index+1:],
			'country_code': url[24:26],
		}
	else:
		if url.find('&uo=') >= 0:
			return {
				'id': url[url.index('?i=')+3:url.index('&uo=')],
				'country_code': url[24:26],
			}
		else:
			return {
				'id': url[url.index('?i=')+3:],
				'country_code': url[24:26],
			}

def get_apple_music_album_id(url: str):
	index = len(url) - 1
	while url[index] != '/':
		index -= 1
	return {
		'id': url[index+1:],
		'country_code': url[24:26],
	}

def get_apple_music_artist(artist_id: str):
	url = f"https://itunes.apple.com/lookup?id={artist_id}"
	response = requests.get(url)
	result = response.json()['results'][0]
	return [result['artistName']]



def search_apple_music_track(artist: str, track: str):
	try:
		tracks_data = []

		url = f"https://itunes.apple.com/search?term={bare_bones(artist)}+{bare_bones(track, False)}&entity=song"
		response = requests.get(url)
		search_results = response.json()['results']

		if search_results != []:
			for result in search_results:
				url = str(result['trackViewUrl'])
				identifier = str(result['trackId'])
				artists = split_artists(str(result['artistName']))
				title = str(result['trackName'])
				cover = str(result['artworkUrl100'])
				tracks_data.append({
					'url': url,
					'id': identifier,
					'artists': artists,
					'track': title,
					'cover': cover,
				})
			return filter_track(artist, track, tracks_data)
		else:
			return None
	except:
		return None



def search_apple_music_album(artist: str, album: str):
	try:
		albums_data = []

		url = f"https://itunes.apple.com/search?term={bare_bones(artist)}+{bare_bones(album, False)}&entity=album"
		response = requests.get(url)
		search_results = response.json()['results']

		if search_results != []:
			for result in search_results:
				url = str(result['collectionViewUrl'])
				identifier = str(result['collectionId'])
				artists = split_artists(str(result['artistName']))
				title = str(result['collectionName'])
				cover = str(result['artworkUrl100'])
				albums_data.append({
					'url': url,
					'id': identifier,
					'artists': artists,
					'album': title,
					'cover': cover,
				})
			return filter_album(artist, album, albums_data)
		else:
			return None
	except:
		return None



def get_apple_music_track(identifier: str, country_code: str):
	try:
		url = f"https://itunes.apple.com/lookup?id={identifier}&country={country_code}"
		response = requests.get(url)
		save_json(response.json())
		result = response.json()['results'][0]
		

		if result != []:
			url = str(result['trackViewUrl'])
			identifier = str(result['trackId'])
			artists = get_apple_music_artist(str(result['artistId']))
			title = str(result['trackName'])
			cover = str(result['artworkUrl100'])
			return {
				'url': url,
				'id': identifier,
				'artists': artists,
				'track': title,
				'cover': cover,
			}
		else:
			return None
	except:
		return None



def get_apple_music_album(identifier: str, country_code: str):
	try:
		url = f"https://itunes.apple.com/lookup?id={identifier}&country={country_code}"
		response = requests.get(url)
		result = response.json()['results'][0]

		if result != []:
			url = str(result['collectionViewUrl'])
			identifier = str(result['collectionId'])
			artists = get_apple_music_artist(str(result['artistId']))
			title = str(result['collectionName'])
			cover = str(result['artworkUrl100'])
			if title.find(' - Single') >= 0:
				return {
					'url': url,
					'id': identifier,
					'artists': artists,
					'track': title.replace(' - Single',''),
					'cover': cover,
				}
			if title.find(' (Apple Music Edition)') >= 0:
				title = title.replace(' (Apple Music Edition)', '')
			if title.find(' - EP') >= 0:
				title = title.replace(' - EP', '')
			return {
				'url': url,
				'id': identifier,
				'artists': artists,
				'album': title,
				'cover': cover,
			}
		else:
			return None
	except:
		return None
