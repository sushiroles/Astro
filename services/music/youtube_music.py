from ytmusicapi import YTMusic
import configparser
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *



config = configparser.ConfigParser()
config.read('tokens.ini')



ytmusic = YTMusic(auth = {
	"scope": str(config['youtube_music']['scope']),
	"token_type": str(config['youtube_music']['token_type']),
	"access_token": str(config['youtube_music']['access_token']),
	"refresh_token": str(config['youtube_music']['refresh_token']),
	"expires_at": int(config['youtube_music']['expires_at']),
	"expires_in": int(config['youtube_music']['expires_in']),
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
		index = url.index('watch?v=') + 8
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



async def get_youtube_music_track(identifier: str):
	try:
		start_time = current_time_ms()
		result = ytmusic.get_song(identifier)['videoDetails']
		if 'musicVideoType' in result:
			if result['musicVideoType'] == 'MUSIC_VIDEO_TYPE_ATV' or result['musicVideoType'] == 'MUSIC_VIDEO_TYPE_OMV':
				track_url = str(f'https://music.youtube.com/watch?v={result['videoId']}')
				track_id = str(result['videoId'])
				track_title = str(result['title'])
				track_artists = split_artists(result['author'])
				track_cover = str(result['thumbnail']['thumbnails'][len(result['thumbnail']['thumbnails'])-1]['url'])
				return {
					'type': 'track',
					'url': track_url,
					'id': track_id,
					'title': track_title,
					'artists': track_artists,
					'cover': track_cover,
					'extra': {
						'api_time_ms': current_time_ms() - start_time,
						'response_status': 'YouTubeMusic-200'
					}
				}
		else:
			return {
				'type': 'empty_response',
			}
	except Exception as response:
		return {
			'type': 'error',
			'response_status': f'YouTubeMusic-"{response}"'
		}



async def get_youtube_music_album(identifier: str):
	try:
		start_time = current_time_ms()
		browse_id = ytmusic.get_album_browse_id(identifier)
		result = ytmusic.get_album(browse_id)
		if 'OLAK5' in identifier[:5]:
			album_url = result['audioPlaylistId']
			album_id = result['audioPlaylistId']
			album_title = result['title']
			album_artists = [artist['name'] for artist in result['artists']]
			album_cover = result['thumbnails'][1]['url']
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
					'response_status': 'YouTubeMusic-200'
				}
			}
		else:
			return {
				'type': 'empty_response',
			}
	except Exception as response:
		return {
			'type': 'error',
			'response_status': f'YouTubeMusic-"{response}"'
		}



async def search_youtube_music_track(artist: str, track: str):
	try:
		tracks_data = []
		start_time = current_time_ms()
		search_results = ytmusic.search(f'{artist} {track}', filter = 'songs')
		for result in search_results:
			if result['resultType'] == 'song':
				track_url = str(f'https://music.youtube.com/watch?v={result['videoId']}')
				track_id = str(result['videoId'])
				track_artists = [artist['name'] for artist in result['artists']]
				track_title = str(result['title'])
				track_cover = str(result['thumbnails'][1]['url'])
				tracks_data.append({
					'type': 'track',
					'url': track_url,
					'id': track_id,
					'title': track_title,
					'artists': track_artists,
					'cover': track_cover,
					'extra': {
						'api_time_ms': current_time_ms() - start_time,
						'response_status': 'YouTubeMusic-200'
					}
				})
		return filter_track(artist = artist, track = track, tracks_data = tracks_data)

	except Exception as response:
		return {
			'type': 'error',
			'response_status': f'YouTubeMusic-"{response}"'
		}



async def search_youtube_music_album(artist: str, album: str):
	try:
		albums_data = []
		start_time = current_time_ms()
		search_results = ytmusic.search(f'{artist} {album}', filter = 'albums')
		for result in search_results:
			if result['resultType'] == 'album':
				browse_id = result['browseId']
				album_artists = [artist['name'] for artist in result['artists']]
				album_title = str(result['title'])
				albums_data.append({
					'type': 'album',
					'browse_id': browse_id,
					'title': album_title,
					'artists': album_artists,
				})
		result = filter_album(artist = artist, album = album, albums_data = albums_data)
		if result['type'] != 'empty_response':
			result = ytmusic.get_album(result['browse_id'])
			album_url = f'https://music.youtube.com/playlist?list={result['audioPlaylistId']}'
			album_id = result['audioPlaylistId']
			album_title = result['title']
			album_artists = [artist['name'] for artist in result['artists']]
			album_cover = result['thumbnails'][1]['url']
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
					'response_status': 'YouTubeMusic-200'
				}
			}
		else:
			return {
				'type': 'empty_response'
			}
	except Exception as response:
		return {
			'type': 'error',
			'response_status': f'YouTubeMusic-"{response}"'
		}
