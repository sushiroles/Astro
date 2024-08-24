from services.music_services import *
from services.etc import *

import asyncio


def is_music(url):
	return (
		is_spotify_track(url)
		or is_spotify_album(url)
		or is_apple_music_track(url)
		or is_apple_music_album(url)
		or is_apple_music_video(url)
		or is_youtube_music_track(url)
		or is_youtube_music_album(url)
		or is_deezer_track(url)
		or is_deezer_album(url)
		or is_tidal_track(url)
		or is_tidal_album(url)
		or is_tidal_video(url)
	)

async def get_music_data(url):
	if is_spotify_track(url):
		identifier = get_spotify_id(url)
		data = await get_spotify_track(identifier)
	elif is_spotify_album(url):
		identifier = get_spotify_id(url)
		data = await get_spotify_album(identifier)
	elif is_apple_music_track(url):
		id_data = get_apple_music_track_id(url)
		data = await get_apple_music_track(id_data['id'], id_data['country_code'])
	elif is_apple_music_album(url):
		id_data = get_apple_music_album_video_id(url)
		data = await get_apple_music_album(id_data['id'], id_data['country_code'])
	elif is_apple_music_video(url):
		id_data = get_apple_music_album_video_id(url)
		data = await get_apple_music_track(id_data['id'], id_data['country_code'])
	elif is_youtube_music_track(url):
		identifier = get_youtube_music_track_id(url)
		data = await get_youtube_music_track(identifier)
	elif is_youtube_music_album(url):
		identifier = get_youtube_music_album_id(url)
		data = await get_youtube_music_album(identifier)
	elif is_deezer_track(url):
		identifier = get_deezer_track_id(url)
		data = await get_deezer_track(identifier)
	elif is_deezer_album(url):
		identifier = get_deezer_album_id(url)
		data = await get_deezer_album(identifier)
	elif is_tidal_track(url):
		identifier = get_tidal_track_id(url)
		data = await get_tidal_track(identifier)
	elif is_tidal_album(url):
		identifier = get_tidal_album_id(url)
		data = await get_tidal_album(identifier)
	elif is_tidal_video(url):
		identifier = get_tidal_video_id(url)
		data = await get_tidal_video(identifier)
	return data



async def get_track_data(service: str, api_call: callable):
	emojis = {
		'Spotify': '<:spotify:1247554944916000839>',
		'Apple Music': '<:applemusic:1247554938733854761>',
		'YouTube Music': '<:youtubemusic:1247554947696955464>',
		'Deezer': '<:deezer:1247554941724397649>',
		'TIDAL': '<:tidal:1247554946123960362>',
	}
	url = ''
	identifier = ''
	artists = []
	title = ''
	cover = ''
	anchor = ''
	log_anchor = ''
	try:
		call_results = await api_call
	except:
		return {
			'url': url,
			'id': identifier,
			'title': title,
			'artists': artists,
			'cover': cover,
			'anchor': anchor,
			'log_anchor': log_anchor
		}
	if call_results['type'] != 'empty_response' and call_results['type'] != 'error':
		url = call_results['url']
		identifier = call_results['id']
		artists = call_results['artists']
		title = call_results['title']
		cover = call_results['cover']
		anchor = f'{emojis[service]} [{service}]({url})\n'
		log_anchor = f'{emojis[service]} [{service}]({url}) ({call_results['extra']['api_time_ms']}ms)\n'
	return {
		'url': url,
		'id': identifier,
		'title': title,
		'artists': artists,
		'cover': cover,
		'anchor': anchor,
		'log_anchor': log_anchor
	}



async def get_album_data(service: str, api_call: callable):
	emojis = {
		'Spotify': '<:spotify:1247554944916000839>',
		'Apple Music': '<:applemusic:1247554938733854761>',
		'YouTube Music': '<:youtubemusic:1247554947696955464>',
		'Deezer': '<:deezer:1247554941724397649>',
		'TIDAL': '<:tidal:1247554946123960362>',
	}
	url = ''
	identifier = ''
	artists = []
	title = ''
	cover = ''
	year = ''
	anchor = ''
	log_anchor = ''
	try:
		call_results = await api_call
	except:
		return {
			'url': url,
			'id': identifier,
			'title': title,
			'artists': artists,
			'cover': cover,
			'year': year,
			'anchor': anchor,
			'log_anchor': log_anchor
		}
	if call_results['type'] != 'empty_response' and call_results['type'] != 'error':
		url = call_results['url']
		identifier = call_results['id']
		title = call_results['title']
		artists = call_results['artists']
		cover = call_results['cover']
		year = call_results['year']
		anchor = f'{emojis[service]} [{service}]({url})\n'
		log_anchor = f'{emojis[service]} [{service}]({url}) ({call_results['extra']['api_time_ms']}ms)\n'
	return {
		'url': url,
		'id': identifier,
		'title': title,
		'artists': artists,
		'cover': cover,
		'year': year,
		'anchor': anchor,
		'log_anchor': log_anchor
	}



async def search_track(artist: str, track: str):
	title = ''
	artists = []
	cover = ''
	requested_artist = artist
	requested_track = track

	service_data = [
		('Spotify', search_spotify_track(artist.replace("'",'').replace(",",''), track.replace("'",'').replace(",",''))),
		('Apple Music', search_apple_music_track(artist, replace_with_ascii(track))),
		('YouTube Music', search_youtube_music_track(artist, track)),
		('Deezer', search_deezer_track(artist, track)),
		('TIDAL', search_tidal_track(artist, track)),
	]
	tasks = [get_track_data(service, function) for service, function in service_data]
	results = await asyncio.gather(*tasks)

	search_results = []
	for result in results:
		search_results.append(result)

	counter = 0
	try:
		while title == '':
			artists = search_results[counter]['artists']
			title = search_results[counter]['title']
			cover = search_results[counter]['cover']
			counter += 1
		anchor = ''.join(result['anchor'] for result in search_results)
		log_anchor = ''.join(result['log_anchor'] for result in search_results)
	except:
		artists = []
		title = ''
		cover = ''
		anchor = ''
		log_anchor = ''

	return {
		'type': 'track',
		'title': title,
		'artists': artists,
		'cover': cover,
		'anchor': anchor,
		'log_anchor': log_anchor,
		'requested_artist': requested_artist,
		'requested_track': requested_track
	}



async def search_album(artist: str, album: str):
	title = ''
	artists = []
	cover = ''
	requested_artist = artist
	requested_album = album

	service_data = [
		('Spotify', search_spotify_album(artist.replace("'",'').replace(",",''), album.replace("'",'').replace(",",''))),
		('Apple Music', search_apple_music_album(artist, replace_with_ascii(album))),
		('YouTube Music', search_youtube_music_album(artist, album)),
		('Deezer', search_deezer_album(artist, album)),
		('TIDAL', search_tidal_album(artist, album)),
	]

	tasks = [get_album_data(service, function) for service, function in service_data]
	results = await asyncio.gather(*tasks)

	search_results = []
	for result in results:
		search_results.append(result)

	counter = 0
	try:
		while title == '':
			artists = search_results[counter]['artists']
			title = search_results[counter]['title']
			cover = search_results[counter]['cover']
			counter += 1
		anchor = ''.join(result['anchor'] for result in search_results)
		log_anchor = ''.join(result['log_anchor'] for result in search_results)
	except:
		artists = []
		title = ''
		cover = ''
		anchor = ''
		log_anchor = ''

	return {
		'type': 'album',
		'title': title,
		'artists': artists,
		'cover': cover,
		'anchor': anchor,
		'log_anchor': log_anchor,
		'requested_artist': requested_artist,
		'requested_album': requested_album,
	}
