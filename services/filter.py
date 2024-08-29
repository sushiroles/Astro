try:
	from services.etc import *
except:
	from etc import *



def filter_track(tracks_data: list, artist: str, track: str, collection: str = None, is_explicit: bool = None):
	artist = bare_bones(artist)
	track = optimize_string(track)
	data_with_percentage = []
	for data in tracks_data:
		data_artists = []
		for name in data['artists']:
			data_artists.append(bare_bones(name))
		artists_string = ' '.join(data_artists)
		data_track = bare_bones(data['title'], False)
		num_of_found_words = 0
		if artists_string.find(artist) >= 0:
			for word in track:
				if data_track.find(word) >= 0:
					num_of_found_words += 1
			similarity_percentage = 100 / len(data_track.split()) * num_of_found_words
			data_with_percentage.append([similarity_percentage, data])
	data_with_percentage = sorted(data_with_percentage, key = lambda x: x[0], reverse = True)
	if data_with_percentage != []:
		return data_with_percentage[0][1]
	else:
		return {
			'type': 'empty_response'
		}

	
def filter_album(albums_data: list, artist: str, album: str, year: str = None):
	artist = bare_bones(artist)
	album = optimize_string(album)
	data_with_percentage = []
	for data in albums_data:
		data_artists = []
		for name in data['artists']:
			data_artists.append(bare_bones(name))
		artists_string = ' '.join(data_artists)
		data_album = bare_bones(data['title'], False)
		num_of_found_words = 0
		if artists_string.find(artist) >= 0:
			for word in album:
				if data_album.find(word) >= 0:
					num_of_found_words += 1
			similarity_percentage = 100 / len(data_album.split()) * num_of_found_words
			data_with_percentage.append([similarity_percentage, data])
	data_with_percentage = sorted(data_with_percentage, key = lambda x: x[0], reverse = True)
	if data_with_percentage != []:
		return data_with_percentage[0][1]
	else:
		return {
			'type': 'empty_response'
		}
