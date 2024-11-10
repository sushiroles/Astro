from ytmusicapi import YTMusic
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *



allowed_track_types = [
	'MUSIC_VIDEO_TYPE_ATV',
	'MUSIC_VIDEO_TYPE_OMV',
	'MUSIC_VIDEO_TYPE_OFFICIAL_SOURCE_MUSIC'
]



ytmusic = YTMusic(auth = {
	"scope": str(tokens['youtube_music']['scope']),
	"token_type": str(tokens['youtube_music']['token_type']),
	"access_token": str(tokens['youtube_music']['access_token']),
	"refresh_token": str(tokens['youtube_music']['refresh_token']),
	"expires_at": int(tokens['youtube_music']['expires_at']),
	"expires_in": int(tokens['youtube_music']['expires_in']),
})



def is_youtube_music_track(url: str):
	return bool(url.find('https://music.youtube.com/watch?v=') >= 0 or url.find('https://www.youtube.com/watch?v=') >= 0 or url.find('https://youtu.be/') >= 0)

def is_youtube_music_album(url: str):
	return bool(url.find('https://music.youtube.com/playlist?list=') >= 0 or url.find('https://www.youtube.com/playlist?list=') >= 0 or url.find('https://youtube.com/playlist?list=') >= 0)

def get_youtube_music_track_id(url: str):
	if url.find('https://youtu.be/') >= 0:
		url = url.replace('https://youtu.be/','')
		if url.find('?') >= 0:
			return str(url[0:url.index('?')])
		else:
			return str(url[0:])
	else:
		index = url.index('v=') + 2
	if url.find('&') >= 0:
		return str(url[index:url.index('&')])
	else:
		return str(url[index:])

def get_youtube_music_album_id(url: str):
	index = url.index('?list=') + 6
	if url.find('&si') >= 0:
		return str(url[index:url.index('&si')])
	else:
		return str(url[index:])

async def get_youtube_music_track_artist(identifier: str):
	try:
		result = ytmusic.get_song(identifier)['videoDetails']
		if 'musicVideoType' in result:
			if result['musicVideoType'] in allowed_track_types:
				try:
					return [ytmusic.get_artist(result['channelId'])['name']]
				except:
					return [result['author']]
	except Exception as response:
		error = {
			'type': 'error',
			'response_status': f'YouTubeMusic-GetTrackArtist-{response}'
		}
		await log('ERROR - YouTube Music API', error['response_status'],f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
		return []



async def get_youtube_music_track(identifier: str):
	try:
		start_time = current_time_ms()
		result = ytmusic.get_song(identifier)['videoDetails']
		if 'musicVideoType' in result:
			if result['musicVideoType'] in allowed_track_types:
				track_url = f'https://music.youtube.com/watch?v={result['videoId']}'
				track_id = result['videoId']
				track_title = remove_music_video_declaration(result['title']) if has_music_video_declaration(result['title']) else result['title']
				track_artists = await get_youtube_music_track_artist(identifier)
				track_cover = result['thumbnail']['thumbnails'][len(result['thumbnail']['thumbnails'])-1]['url']
				return {
					'type': 'track',
					'url': track_url,
					'id': track_id,
					'title': track_title,
					'artists': track_artists,
					'cover': track_cover,
					'collection_name': None,
					'is_explicit': None,
					'extra': {
						'api_time_ms': current_time_ms() - start_time,
						'response_status': 'YouTubeMusic-GetTrack-200'
					}
				}
		else:
			await log('NOTICE - YouTube Music API', f'Empty response (either broken MV or non-MV video)', f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
			return {
				'type': 'empty_response',
			}
	except Exception as response:
		error = {
			'type': 'error',
			'response_status': f'YouTubeMusic-GetTrack-{response}'
		}
		await log('ERROR - YouTube Music API', error['response_status'],f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
		return error



async def get_youtube_music_album(identifier: str):
	try:
		start_time = current_time_ms()
		browse_id = ytmusic.get_album_browse_id(identifier)
		result = ytmusic.get_album(browse_id)
		if 'OLAK5' in identifier[:5]:
			album_url = f'https://music.youtube.com/playlist?list={result['audioPlaylistId']}'
			album_id = result['audioPlaylistId']
			album_title = result['title']
			album_artists = [artist['name'] for artist in result['artists']]
			album_cover = result['thumbnails'][len(result['thumbnails'])-1]['url']
			album_year = result['year']
			return {
				'type': 'album',
				'url': album_url,
				'id': album_id,
				'title': album_title,
				'artists': album_artists,
				'cover': album_cover,
				'year': album_year,
				'extra': {
					'api_time_ms': current_time_ms() - start_time,
					'response_status': 'YouTubeMusic-GetAlbum-200'
				}
			}
		else:
			return {
				'type': 'empty_response',
			}
	except Exception as response:
		error = {
			'type': 'error',
			'response_status': f'YouTubeMusic-GetAlbum-{response}'
		}
		await log('ERROR - YouTube Music API', error['response_status'],f'ID: `{identifier}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
		return error



async def search_youtube_music_track(artist: str, track: str, collection: str = None, is_explicit: bool = None):
	artist = optimize_for_search(artist)
	track = optimize_for_search(track)
	collection = clean_up_collection_title(optimize_for_search(collection)) if collection != None else None
	try:
		tracks_data = []
		start_time = current_time_ms()
		search_results = ytmusic.search(artist + ' ' + track, filter = 'songs')
		for result in search_results:
			if result['resultType'] == 'song':
				track_url = f'https://music.youtube.com/watch?v={result['videoId']}'
				track_id = result['videoId']
				track_title = result['title']
				track_artists = [artist['name'] for artist in result['artists']] if result['artists'] != [] else await get_youtube_music_track_artist(result['videoId'])
				track_cover = result['thumbnails'][len(result['thumbnails'])-1]['url']
				track_collection = result['album']['name']
				track_is_explicit = result['isExplicit']
				tracks_data.append({
					'type': 'track',
					'url': track_url,
					'id': track_id,
					'title': track_title,
					'artists': track_artists,
					'cover': track_cover,
					'collection_name': track_collection,
					'is_explicit': track_is_explicit,
					'extra': {
						'api_time_ms': current_time_ms() - start_time,
						'response_status': 'YouTubeMusic-SearchTrack-200'
					}
				})
		return filter_track(tracks_data = tracks_data, artist = artist, track = track, collection = collection, is_explicit = is_explicit)
	except Exception as response:
		error = {
			'type': 'error',
			'response_status': f'YouTubeMusic-SearchTrack-{response}'
		}
		await log('ERROR - YouTube Music API', error['response_status'],f'Artist: `{artist}`\nTrack: `{track}`\nCollection: `{collection}`\nIs explicit? `{is_explicit}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
		return error



async def search_youtube_music_album(artist: str, album: str, year: str = None):
	artist = optimize_for_search(artist)
	album = optimize_for_search(album)
	try:
		albums_data = []
		start_time = current_time_ms()
		search_results = ytmusic.search(artist + ' ' + album, filter = 'albums')
		for result in search_results:
			if result['resultType'] == 'album':
				album_url = f'https://music.youtube.com/playlist?list={result['playlistId']}'
				album_id = result['playlistId']
				album_title = result['title']
				album_artists = [artist['name'] for artist in result['artists']]
				album_cover = result['thumbnails'][len(result['thumbnails'])-1]['url']
				album_year = result['year']
				albums_data.append({
					'type': 'album',
					'url': album_url,
					'id': album_id,
					'title': album_title,
					'artists': album_artists,
					'cover': album_cover,
					'year': album_year,
					'extra': {
						'api_time_ms': current_time_ms() - start_time,
						'response_status': 'YouTubeMusic-SearchAlbum-200'
					}
				})
		return filter_album(albums_data = albums_data, artist = artist, album = album, year = year)
	except Exception as response:
		error = {
			'type': 'error',
			'response_status': f'YouTubeMusic-SearchAlbum-{response}'
		}
		await log('ERROR - YouTube Music API', error['response_status'],f'Artist: `{artist}`\nTrack: `{track}`Year: `{year}`', logs_channel = (tokens['discord']['internal_logs_channel'] if bool(tokens['discord']['is_internal'] == 'True') else tokens['discord']['logs_channel']))
		return error
