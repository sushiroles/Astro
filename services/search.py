from services.spotify import *
from services.apple_music import *
from services.youtube_music import *
from services.deezer import *
from services.tidal import *
from services.bandcamp import *
from services.etc import *

import functools
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
	elif is_bandcamp_track(url):
		data = get_bandcamp_track_parameters(url)
		url_type = 'track'
	elif is_bandcamp_album(url):
		data = get_bandcamp_album_parameters(url)
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
		'Bandcamp': '<:bandcamp:1247554940071841803>',
	}
	try:
		call_results = api_call
		url = call_results['url']
		identifier = call_results['id']
		artists = call_results['artists']
		track = call_results['track']
		year = call_results['year']
		cover = call_results['cover']
		anchor = f'{emojis[service]} [{service}]({url})\n'
	except Exception as error:
		url = ''
		identifier = ''
		artists = []
		track = ''
		year = ''
		cover = ''
		anchor = ''
	results.append({
		'url': url,
		'id': identifier,
		'artists': artists,
		'track': track,
		'year': year,
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
		'Bandcamp': '<:bandcamp:1247554940071841803>',
	}
	try:
		call_results = api_call
		url = call_results['url']
		identifier = call_results['id']
		artists = call_results['artists']
		album = call_results['album']
		year = call_results['year']
		cover = call_results['cover']
		anchor = f'{emojis[service]} [{service}]({url})\n'
	except Exception as error:
		url = ''
		identifier = ''
		artists = []
		album = ''
		year = ''
		cover = ''
		anchor = ''
	results.append({
		'url': url,
		'id': identifier,
		'artists': artists,
		'album': album,
		'year': year,
		'cover': cover,
		'anchor': anchor,
	})



@functools.cache
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
		('Bandcamp', search_bandcamp_track(bare_bones(artist), bare_bones(track))),
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



@functools.cache
def search_album(artist: str, album: str):
	artists = []
	title = ''
	cover = ''
	requested_artist = artist
	requested_album = album

	service_data = [
		('Spotify', search_spotify_album(artist, album)),
		('Apple Music', search_apple_music_album(artist, album)),
		('YouTube Music', search_youtube_music_album(artist, album)),
		('Deezer', search_deezer_album(artist, album)),
		('TIDAL', search_tidal_album(artist, album)),
		('Bandcamp', search_bandcamp_album(artist, album)),
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
