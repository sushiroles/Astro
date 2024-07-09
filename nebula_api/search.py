from nebula_api.spotify_nebula import *
from nebula_api.apple_music_nebula import *
from nebula_api.youtube_music_nebula import *
from nebula_api.deezer_nebula import *
from nebula_api.tidal_nebula import *
from nebula_api.bandcamp_nebula import *
from nebula_api.etc import *

import functools
import threading

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
		log('ERROR', f'Inside get_track_data(): "{error}" --- service: {service}')
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
		log('ERROR', f'Inside get_album_data(): "{error}" --- service: {service} / api_call: {str(api_call)}')
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
		thread = threading.Thread(target=get_track_data, args=(service, function, results))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()

	search_results = []
	for result in results:
		search_results.append(result)

	counter = 0
	while title == '':
		try:
			artists = search_results[counter]['artists']
			title = search_results[counter]['track']
			cover = search_results[counter]['cover']
			counter += 1
		except:
			pass

	anchor = ''.join(result['anchor'] for result in search_results)	



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
		('Spotify', search_spotify_album(bare_bones(artist), bare_bones(album))),
		('Apple Music', search_apple_music_album(bare_bones(artist), bare_bones(album))),
		('YouTube Music', search_youtube_music_album(bare_bones(artist), bare_bones(album))),
		('Deezer', search_deezer_album(bare_bones(artist), bare_bones(album))),
		('TIDAL', search_tidal_album(bare_bones(artist), bare_bones(album))),
		('Bandcamp', search_bandcamp_album(bare_bones(artist), bare_bones(album))),
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
	while title == '':
		try:
			artists = search_results[counter]['artists']
			title = search_results[counter]['album']
			cover = search_results[counter]['cover']
			print(title)
			counter += 1
		except:
			pass
	
	anchor = ''.join(result['anchor'] for result in search_results)	



	return [{
		'cover': cover,
		'artists': artists,
		'album': title,
		'anchor': anchor,

		'requested_artist': requested_artist,
		'requested_album': requested_album,
	}]
