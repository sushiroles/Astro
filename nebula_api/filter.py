try:
	from nebula_api.etc import *
except:
	from etc import *

def filter_track(artist: str, track: str, tracks_data: list):
	artist = bare_bones(artist)
	track = bare_bones(track)
	for data in tracks_data:
		data_artists = []
		for name in data['artists']:
			data_artists.append(bare_bones(name))
		artists_string = ' '.join(data_artists)
		data_track = bare_bones(data['track'])
		if artists_string.find(artist) >= 0 and data_track.find(track) >= 0:
			return data
	return None

def filter_album(artist: str, album: str, albums_data: list):
	artist = bare_bones(artist)
	album = bare_bones(album)
	for data in albums_data:
		data_artists = []
		for name in data['artists']:
			data_artists.append(bare_bones(name))
		artists_string = ' '.join(data_artists)
		data_track = bare_bones(data['album'])
		if artists_string.find(artist) >= 0 and data_track.find(album) >= 0:
			return data
	return None


# WIP
def album_honesty_filter(spotify_data, apple_music_data, youtube_music_data, deezer_data, tidal_data, bandcamp_data):
	spotify = 0
	apple_music = 1
	youtube_music = 2
	deezer = 3
	tidal = 4
	bandcamp = 5

	artist_names = [spotify_data['artist']]
	album_names = []
	release_years = []