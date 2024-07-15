import requests
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *



def is_apple_music_track(url: str):
	return bool(url.find('https://music.apple.com/') >= 0 and url.find('?i=') >= 0)

def is_apple_music_album(url: str):
	return bool(url.find('https://music.apple.com/') >= 0 and not url.find('?i=') >= 0)

def get_apple_music_track_id(url: str):
	index = url.index('?i=') + 3
	if url.find('&uo=') >= 0:
		return url[index:url.index('&uo=')]
	else:
		return url[index:]

def get_apple_music_album_id(url: str):
	index = len(url) - 1
	while url[index] != '/':
		index -= 1
	return url[index+1:]


	
def search_apple_music_track(artist, track):
	try:
		tracks_data = []

		url = f"https://itunes.apple.com/search?term={bare_bones(artist).replace(' ','+')}+{bare_bones(track).replace(' ','+')}&entity=song"
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
	except:
		return None



def search_apple_music_album(artist, album):
	try:
		albums_data = []

		url = f"https://itunes.apple.com/search?term={bare_bones(artist).replace(' ','+')}+{bare_bones(album).replace(' ','+')}&entity=album"
		response = requests.get(url)
		save_json(response.json())
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
	except Exception as e:
		print(e)
		return None



def get_apple_music_track(identifier: str):
	try:
		url = f"https://itunes.apple.com/lookup?id={identifier}"
		response = requests.get(url)
		result = response.json()['results'][0]

		if result != []:
			url = str(result['trackViewUrl'])
			identifier = str(result['trackId'])
			artists = split_artists(str(result['artistName']))
			title = str(result['trackName'])
			if title.lower().find('feat. ') >= 0:
				title = title[:title.index('feat. ')-2]
			year = str(result['releaseDate'][:4])
			cover = str(result['artworkUrl100'])
			return {
				'url': url,
				'id': identifier,
				'artists': artists,
				'track': title,
				'year': year,
				'cover': cover,
			}
		else:
			return None
	except:
		return None



def get_apple_music_album(identifier: str):
	try:
		url = f"https://itunes.apple.com/lookup?id={identifier}"
		response = requests.get(url)
		result = response.json()['results'][0]

		if result != []:
			url = str(result['collectionViewUrl'])
			identifier = str(result['collectionId'])
			artists = split_artists(str(result['artistName']))
			title = str(result['collectionName'])
			if title.find(' - EP') >= 0:
				title = title.replace(' - EP', '')
			year = str(result['releaseDate'][:4])
			cover = str(result['artworkUrl100'])
			return {
				'url': url,
				'id': identifier,
				'artists': artists,
				'album': title,
				'year': year,
				'cover': cover,
			}
		else:
			return None
	except:
		return None
