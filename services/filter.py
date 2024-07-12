try:
	from services.etc import *
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
	services = {
		'Spotify': 0,
		'Apple Music': 1,
		'Youtube Music': 2,
		'Deezer': 3,
		'TIDAL': 4,
		'Bandcamp': 5,
	}
	
	artist_names = [
		bare_bones(' '.join(spotify_data['artists'])),
		bare_bones(' '.join(apple_music_data['artists'])),
		bare_bones(' '.join(youtube_music_data['artists'])),
		bare_bones(' '.join(deezer_data['artists'])),
		bare_bones(' '.join(tidal_data['artists'])),
		bare_bones(' '.join(bandcamp_data['artists'])),
	]
	print(artist_names)
	album_titles = [
		spotify_data['album'],
		apple_music_data['album'],
		youtube_music_data['album'],
		deezer_data['album'],
		tidal_data['album'],
		bandcamp_data['album'],
	]
	release_years = [
		spotify_data['year'],
		apple_music_data['year'],
		youtube_music_data['year'],
		deezer_data['year'],
		tidal_data['year'],
		bandcamp_data['year'],
	]
	anchors = [
		spotify_data['anchor'],
		apple_music_data['anchor'],
		youtube_music_data['anchor'],
		deezer_data['anchor'],
		tidal_data['anchor'],
		bandcamp_data['anchor'],
	]

	common_artist_data = get_common_data(artist_names)
	common_title_data = get_common_data(album_titles)
	common_year_data = get_common_data(release_years)

	final_anchors = ''
	
	for i in range(len(services)):
		if bare_bones(common_title_data) == bare_bones(album_titles[i]):
			if common_year_data == release_years[i] or release_years == '':
				final_anchors += anchors[i]
	return final_anchors

