try:
	from services.etc import *
except:
	from etc import *



def filter_track(artist: str, track: str, tracks_data: list):
	artist = bare_bones(artist)
	track = bare_bones(track, False)
	for scans in range(2):
		for data in tracks_data:
			data_artists = []
			for name in data['artists']:
				data_artists.append(bare_bones(name, True))
			artists_string = ' '.join(data_artists)
			data_track = bare_bones(data['track'], False)		
			if scans == 0:
				condition = artists_string.find(artist) >= 0 and data_track == track
			else:
				condition = artists_string.find(artist) >= 0 and data_track.find(track) >= 0
			if condition:
				return data
	return None



def filter_album(artist: str, album: str, albums_data: list):
	artist = bare_bones(artist)
	album = bare_bones(album, False)
	for scans in range(2):
		for data in albums_data:
			data_artists = []
			for name in data['artists']:
				data_artists.append(bare_bones(name))
			artists_string = ' '.join(data_artists)
			data_album = bare_bones(data['album'], False)
			if scans == 0:
				condition = artists_string.find(artist) >= 0 and data_album == album
			else:
				condition = artists_string.find(artist) >= 0 and data_album.find(album) >= 0
			if condition:
				return data
	return None
