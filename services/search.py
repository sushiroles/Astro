from services.spotify import *
from services.apple_music import *
from services.youtube_music import *
from services.deezer import *
from services.tidal import *
from services.etc import *

import threading



def get_music_data(url):
	if is_spotify_track(url):
		identifier = get_spotify_id(url)
		data = get_spotify_track(identifier)
		url_type = 'track'
	elif is_spotify_album(url):
		identifier = get_spotify_id(url)
		data = get_spotify_album(identifier)
		url_type = 'album'
	elif is_apple_music_track(url):
		id_data = get_apple_music_track_id(url)
		data = get_apple_music_track(id_data['id'], id_data['country_code'])
		url_type = 'track'
	elif is_apple_music_album(url):
		id_data = get_apple_music_album_id(url)
		data = get_apple_music_album(id_data['id'], id_data['country_code'])
		if 'track' in data:
			url_type = 'track'
		else:
			url_type = 'album'
	elif is_youtube_music_track(url):
		identifier = get_youtube_music_track_id(url)
		data = get_youtube_music_track(identifier)
		url_type = 'track'
	elif is_youtube_music_album(url):
		identifier = get_youtube_music_album_id(url)
		data = get_youtube_music_album(identifier)
		url_type = 'album'
	elif is_deezer_track(url):
		identifier = get_deezer_track_id(url)
		data = get_deezer_track(identifier)
		url_type = 'track'
	elif is_deezer_album(url):
		identifier = get_deezer_album_id(url)
		data = get_deezer_album(identifier)
		url_type = 'album'
	elif is_tidal_track(url):
		identifier = get_tidal_track_id(url)
		data = get_tidal_track(identifier)
		url_type = 'track'
	elif is_tidal_album(url):
		identifier = get_tidal_album_id(url)
		data = get_tidal_album(identifier)
		url_type = 'album'
	return {
		'data': data,
		'url_type': url_type,
	}



def get_track_data(service: str, api_call: callable, results: list):
	emojis = {
		'Spotify': '<:spotify:1247554944916000839>',
		'Apple Music': '<:applemusic:1247554938733854761>',
		'YouTube Music': '<:youtubemusic:1247554947696955464>',
		'Deezer': '<:deezer:1247554941724397649>',
		'TIDAL': '<:tidal:1247554946123960362>',
	}
	try:
		call_results = api_call
		url = call_results['url']
		identifier = call_results['id']
		artists = call_results['artists']
		track = call_results['track']
		cover = call_results['cover']
		anchor = f'{emojis[service]} [{service}]({url})\n'
	except:
		url = ''
		identifier = ''
		artists = []
		track = ''
		cover = ''
		anchor = ''
	results.append({
		'url': url,
		'id': identifier,
		'artists': artists,
		'track': track,
		'cover': cover,
		'anchor': anchor,
	})



def get_album_data(service: str, api_call: callable, results: list):
	emojis = {
		'Spotify': '<:spotify:1247554944916000839>',
		'Apple Music': '<:applemusic:1247554938733854761>',
		'YouTube Music': '<:youtubemusic:1247554947696955464>',
		'Deezer': '<:deezer:1247554941724397649>',
		'TIDAL': '<:tidal:1247554946123960362>',
	}
	try:
		call_results = api_call
		url = call_results['url']
		identifier = call_results['id']
		artists = call_results['artists']
		album = call_results['album']
		cover = call_results['cover']
		anchor = f'{emojis[service]} [{service}]({url})\n'
	except:
		url = ''
		identifier = ''
		artists = []
		album = ''
		cover = ''
		anchor = ''
	results.append({
		'url': url,
		'id': identifier,
		'artists': artists,
		'album': album,
		'cover': cover,
		'anchor': anchor,
	})



def search_track(artist: str, track: str):
	artists = []
	title = ''
	cover = ''
	requested_artist = artist
	requested_track = track

	service_data = [
		('Spotify', search_spotify_track(bare_bones(artist), bare_bones(track))),
		('Apple Music', search_apple_music_track(bare_bones(artist), bare_bones(track))),
		('YouTube Music', search_youtube_music_track(bare_bones(artist), bare_bones(track))),
		('Deezer', search_deezer_track(bare_bones(artist), bare_bones(track))),
		('TIDAL', search_tidal_track(bare_bones(artist), bare_bones(track))),
	]

	threads = []
	results = []
	for service, function in service_data:
		thread = threading.Thread(target = get_track_data, args = (service, function, results))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()

	search_results = []
	for result in results:
		search_results.append(result)

	counter = 0
	try:
		while title == '':
			artists = search_results[counter]['artists']
			title = search_results[counter]['track']
			cover = search_results[counter]['cover']
			counter += 1
		anchor = ''.join(result['anchor'] for result in search_results)
	except:
		artists = []
		title = ''
		cover = ''
		anchor = ''



	return [{
		'cover': cover,
		'artists': artists,
		'track': title,
		'anchor': anchor,
		'requested_artist': requested_artist,
		'requested_track': requested_track,
	}]



def search_album(artist: str, album: str):
	artists = []
	title = ''
	cover = ''
	requested_artist = artist
	requested_album = album

	service_data = [
		('Spotify', search_spotify_album(bare_bones(artist), bare_bones(album))),
		('Apple Music', search_apple_music_album(artist, album)),
		('YouTube Music', search_youtube_music_album(artist, album)),
		('Deezer', search_deezer_album(artist, album)),
		('TIDAL', search_tidal_album(artist, album)),
	]

	threads = []
	results = []
	for service, function in service_data:
		thread = threading.Thread(target=get_album_data, args=(service, function, results))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()

	search_results = []
	for result in results:
		search_results.append(result)

	counter = 0
	try:
		while title == '':
			artists = search_results[counter]['artists']
			title = search_results[counter]['album']
			cover = search_results[counter]['cover']
			counter += 1
		anchor = ''.join(result['anchor'] for result in search_results)	
	except:
		artists = []
		title = ''
		cover = ''
		anchor = ''



	return [{
		'cover': cover,
		'artists': artists,
		'album': title,
		'anchor': anchor,
		'requested_artist': requested_artist,
		'requested_album': requested_album,
	}]



def search_track_from_url_data(artist: str, track: str):
	artists = []
	title = ''
	cover = ''
	requested_artist = artist
	requested_track = track

	service_data = [
		('Spotify', search_spotify_track(artist.replace("'",''), track.replace("'",''))),
		('Apple Music', search_apple_music_track(replace_with_ascii(artist), replace_with_ascii(track))),
		('YouTube Music', search_youtube_music_track(artist, track)),
		('Deezer', search_deezer_track(artist, track)),
		('TIDAL', search_tidal_track(artist, track)),
	]

	threads = []
	results = []
	for service, function in service_data:
		thread = threading.Thread(target = get_track_data, args = (service, function, results))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()



	search_results = []
	for result in results:
		search_results.append(result)

	counter = 0
	try:
		while title == '':
			artists = search_results[counter]['artists']
			title = search_results[counter]['track']
			cover = search_results[counter]['cover']
			counter += 1
		anchor = ''.join(result['anchor'] for result in search_results)
	except:
		artists = []
		title = ''
		cover = ''
		anchor = ''



	return [{
		'cover': cover,
		'artists': artists,
		'track': title,
		'anchor': anchor,
		'requested_artist': requested_artist,
		'requested_track': requested_track,
	}]



def search_album_from_url_data(artist: str, album: str):
	artists = []
	title = ''
	cover = ''
	requested_artist = artist
	requested_album = album

	service_data = [
		('Spotify', search_spotify_album(artist.replace("'",''), album.replace("'",''))),
		('Apple Music', search_apple_music_album(replace_with_ascii(artist), replace_with_ascii(album))),
		('YouTube Music', search_youtube_music_album(artist, album)),
		('Deezer', search_deezer_album(artist, album)),
		('TIDAL', search_tidal_album(artist, album)),
	]

	threads = []
	results = []
	for service, function in service_data:
		thread = threading.Thread(target = get_album_data, args = (service, function, results))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()



	search_results = []
	for result in results:
		search_results.append(result)

	counter = 0
	try:
		while title == '':
			artists = search_results[counter]['artists']
			title = search_results[counter]['album']
			cover = search_results[counter]['cover']
			counter += 1
		anchor = ''.join(result['anchor'] for result in search_results)	
	except:
		artists = []
		title = ''
		cover = ''
		anchor = ''



	return [{
		'cover': cover,
		'artists': artists,
		'album': title,
		'anchor': anchor,
		'requested_artist': requested_artist,
		'requested_album': requested_album,
	}]
