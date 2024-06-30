from nebula_api.spotify_nebula import *
from nebula_api.apple_music_nebula import *
from nebula_api.youtube_music_nebula import *
from nebula_api.deezer_nebula import *
from nebula_api.tidal_nebula import *
from nebula_api.bandcamp_nebula import *
from nebula_api.etc import *

import functools

def get_track_data(service: str, api_call: callable):
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
		log('ERROR', f'Inside get_track_data(): "{error}" --- service: {service} / api_call: {str(api_call)}')
	return {
		'url': url,
		'id': identifier,
		'artists': artists,
		'track': track,
		'year': year,
		'cover': cover,
		'anchor': anchor,
	}

def get_album_data(service: str, api_call: callable):
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
	return {
		'url': url,
		'id': identifier,
		'artists': artists,
		'album': album,
		'year': year,
		'cover': cover,
		'anchor': anchor,
	}


@functools.cache
def search_track(artist: str, track: str):
	artist_name = ''
	track_name = ''
	cover_art = ''
	requested_artist = artist
	requested_track = track


	# Search on Spotify
	spotify = get_track_data('Spotify', search_spotify_track(bare_bones(artist),bare_bones(track)))
	if artist_name == '' and track_name == '': 
		artist_name = spotify['artists']
		track_name = spotify['track']

	# Search on Apple Music
	apple_music = get_track_data('Apple Music', search_apple_music_track(bare_bones(artist),bare_bones(track)))
	if artist_name == '' and track_name == '': 
		artist_name = apple_music['artists']
		track_name = apple_music['track']

	# Search on YouTube Music
	youtube_music = get_track_data('YouTube Music', search_youtube_music_track(bare_bones(artist),bare_bones(track)))
	if artist_name == '' and track_name == '': 
		artist_name = youtube_music['artists']
		track_name = youtube_music['track']

	# Search on Deezer
	deezer = get_track_data('Deezer', search_deezer_track(bare_bones(artist),bare_bones(track)))
	if artist_name == '' and track_name == '': 
		artist_name = deezer['artists']
		track_name = deezer['track']

	# Search on TIDAL
	tidal = get_track_data('TIDAL', search_tidal_track(bare_bones(artist),bare_bones(track)))
	if artist_name == '' and track_name == '': 
		artist_name = tidal['artists']
		track_name = tidal['track']

	# Bandcamp
	bandcamp = get_track_data('Bandcamp', search_bandcamp_track(bare_bones(artist),bare_bones(track)))
	if artist_name == '' and track_name == '': 
		artist_name = bandcamp['artists']
		track_name = bandcamp['track']

	cover_art = spotify['cover']
	service_anchor = f'{spotify['anchor']}{apple_music['anchor']}{youtube_music['anchor']}{deezer['anchor']}{tidal['anchor']}{bandcamp['anchor']}'

	return [{
		'cover_art': cover_art,
		'artist_name': artist_name,
		'track_name': track_name,
		'service_anchor': service_anchor,

		'requested_artist': requested_artist,
		'requested_track': requested_track,

		'spotify_url': spotify['url'],
		'spotify_id': spotify['id'],

		'apple_music_url': apple_music['url'],
		'apple_music_id': apple_music['id'],

		'youtube_music_url': youtube_music['url'],
		'youtube_music_id': youtube_music['id'],

		'deezer_url': deezer['url'],
		'deezer_id': deezer['id'],

		'tidal_url': tidal['url'],
		'tidal_id': tidal['id'],
		
		'bandcamp_url': bandcamp['url'],
		'bandcamp_id': bandcamp['id'],
	}]

@functools.cache
def search_album(artist: str, album: str):
	artist_name = ''
	album_name = ''
	cover_art = ''
	requested_artist = artist
	requested_album = album


	# Search on Spotify
	spotify = get_album_data('Spotify', search_spotify_album(bare_bones(artist),bare_bones(album)))
	if artist_name == '' and album_name == '': 
		artist_name = spotify['artists']
		album_name = spotify['album']

	# Search on Apple Music
	apple_music = get_album_data('Apple Music', search_apple_music_album(bare_bones(artist),bare_bones(album)))
	if artist_name == '' and album_name == '': 
		artist_name = apple_music['artists']
		album_name = apple_music['album']

	# Search on YouTube Music
	youtube_music = get_album_data('YouTube Music', search_youtube_music_album(bare_bones(artist),bare_bones(album)))
	if artist_name == '' and album_name == '': 
		artist_name = youtube_music['artists']
		album_name = youtube_music['album']

	# Search on Deezer
	deezer = get_album_data('Deezer', search_deezer_album(bare_bones(artist),bare_bones(album)))
	if artist_name == '' and album_name == '': 
		artist_name = deezer['artists']
		album_name = deezer['album']
	
	# Search on TIDAL
	tidal = get_album_data('TIDAL', search_tidal_album(bare_bones(artist),bare_bones(album)))
	if artist_name == '' and album_name == '': 
		artist_name = tidal['artists']
		album_name = tidal['album']

	# Bandcamp
	bandcamp = get_album_data('Bandcamp', search_bandcamp_album(bare_bones(artist),bare_bones(album)))
	if artist_name == '' and album_name == '': 
		artist_name = bandcamp['artists']
		album_name = bandcamp['album']

	cover_art = spotify['cover']
	service_anchor = f'{spotify['anchor']}{apple_music['anchor']}{youtube_music['anchor']}{deezer['anchor']}{tidal['anchor']}{bandcamp['anchor']}'

	return [{
		'cover_art': cover_art,
		'artist_name': artist_name,
		'album_name': album_name,
		'service_anchor': service_anchor,

		'requested_artist': requested_artist,
		'requested_album': requested_album,

		'spotify_url': spotify['url'],
		'spotify_id': spotify['id'],

		'apple_music_url': apple_music['url'],
		'apple_music_id': apple_music['id'],

		'youtube_music_url': youtube_music['url'],
		'youtube_music_id': youtube_music['id'],

		'deezer_url': deezer['url'],
		'deezer_id': deezer['id'],

		'tidal_url': tidal['url'],
		'tidal_id': tidal['id'],

		'bandcamp_url': bandcamp['url'],
		'bandcamp_id': bandcamp['id'],
	}]
