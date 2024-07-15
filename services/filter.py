try:
	from services.etc import *
except:
	from etc import *

def filter_track(artist: str, track: str, tracks_data: list):
	artist = bare_bones(artist)
	track = bare_bones(track)
	for scans in range(2):
		for data in tracks_data:
			data_artists = []
			for name in data['artists']:
				data_artists.append(bare_bones(name))
			artists_string = ' '.join(data_artists)
			data_track = bare_bones(data['track'])
			if scans == 0:
				condition = artists_string.find(artist) >= 0 and data_track == track
			else:
				condition = artists_string.find(artist) >= 0 and data_track.find(track) >= 0
			if condition:
				return data
	return None

def filter_album(artist: str, album: str, albums_data: list):
	artist = bare_bones(artist)
	album = bare_bones(album)
	for scans in range(2):
		for data in albums_data:
			data_artists = []
			for name in data['artists']:
				data_artists.append(bare_bones(name))
			artists_string = ' '.join(data_artists)
			data_album = bare_bones(data['album'])
			if scans == 0:
				condition = artists_string.find(artist) >= 0 and data_album == album
			else:
				condition = artists_string.find(artist) >= 0 and data_album.find(album) >= 0
			if condition:
				return data
	return None

def track_honesty_filter(spotify_data, apple_music_data, youtube_music_data, deezer_data, tidal_data, bandcamp_data):
	artist_names = [
		bare_bones(' '.join(spotify_data['artists'])),
		bare_bones(' '.join(apple_music_data['artists'])),
		bare_bones(' '.join(youtube_music_data['artists'])),
		bare_bones(' '.join(deezer_data['artists'])),
		bare_bones(' '.join(tidal_data['artists'])),
		bare_bones(' '.join(bandcamp_data['artists'])),
	]

	track_titles = [
		bare_bones(spotify_data['track']),
		bare_bones(apple_music_data['track']),
		bare_bones(youtube_music_data['track']),
		bare_bones(deezer_data['track']),
		bare_bones(tidal_data['track']),
		bare_bones(bandcamp_data['track']),
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

	honest_anchors = []
	honesty_counter = 0

	common_artist_data = get_common_data(artist_names)
	common_title_data = get_common_data(track_titles)
	common_year_data = get_common_data(release_years)
	print(common_artist_data)
	print(common_title_data)
	print(common_year_data)

	for anchor in anchors:
		if artist_names[honesty_counter] == common_artist_data:
			if track_titles[honesty_counter] == common_title_data:
				honest_anchors.append(anchor)
				honesty_counter += 1

	return honest_anchors

def album_honesty_filter(spotify_data, apple_music_data, youtube_music_data, deezer_data, tidal_data, bandcamp_data):
	artist_names = [
		bare_bones(' '.join(spotify_data['artists'])),
		bare_bones(' '.join(apple_music_data['artists'])),
		bare_bones(' '.join(youtube_music_data['artists'])),
		bare_bones(' '.join(deezer_data['artists'])),
		bare_bones(' '.join(tidal_data['artists'])),
		bare_bones(' '.join(bandcamp_data['artists'])),
	]

	album_titles = [
		bare_bones(spotify_data['album']),
		bare_bones(apple_music_data['album']),
		bare_bones(youtube_music_data['album']),
		bare_bones(deezer_data['album']),
		bare_bones(tidal_data['album']),
		bare_bones(bandcamp_data['album']),
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

	honest_anchors = []
	honesty_counter = 0

	common_artist_data = get_common_data(artist_names)
	common_title_data = get_common_data(album_titles)
	common_year_data = get_common_data(release_years)

	for anchor in anchors:
		if artist_names[honesty_counter] == common_artist_data:
			if album_titles[honesty_counter] == common_title_data:
				if release_years[honesty_counter] == common_year_data or release_years[honesty_counter] == '':
					honest_anchors.append(anchor)
					honesty_counter += 1

	return honest_anchors
