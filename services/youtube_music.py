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
	return bool(url.find('https://music.youtube.com/watch?v=') >= 0 or url.find('https://www.youtube.com/watch?v=') >= 0)
 
def is_youtube_music_album(url: str):
	return bool(url.find('https://music.youtube.com/playlist?list=') >= 0 or url.find('https://www.youtube.com/playlist?list=') >= 0)

def get_youtube_music_track_id(url: str):
	index = url.index('watch?v=') + 8
	if url.find('&') >= 0:
		return str(url[index:url.index('&')])
	else:
		return str(url[index:])

def get_youtube_music_album_id(url: str):
	index = url.index('?list=') + 6
	return str(url[index:])



async def get_youtube_music_track(identifier: str):
	try:
		result = ytmusic.get_song(identifier)['videoDetails']
		if result['musicVideoType'] == 'MUSIC_VIDEO_TYPE_ATV' or result['musicVideoType'] == 'MUSIC_VIDEO_TYPE_OMV':
			url = str(f'https://music.youtube.com/watch?v={result['videoId']}')
			identifier = str(result['videoId'])
			artists = split_artists(result['author'])
			title = str(result['title'])
			cover = str(result['thumbnail']['thumbnails'][len(result['thumbnail']['thumbnails'])-1]['url'])
			return {
				'url': url,
				'id': identifier,
				'artists': artists,
				'track': title,
				'cover': cover,
			}
	except:
		return None



async def get_youtube_music_album(identifier: str):
	try:
		browse_id = ytmusic.get_album_browse_id(identifier)
		result = ytmusic.get_album(browse_id)
		if 'OLAK5' in identifier[:5]:
			url = str(result['audioPlaylistId'])
			identifier = str(result['audioPlaylistId'])
			artists = []
			for names in result['artists']:
				artists.append(str(names['name']))
			title = str(result['title'])
			cover = str(result['thumbnails'][1]['url'])
			return {
				'url': url,
				'id': identifier,
				'artists': artists,
				'album': title,
				'cover': cover,
			}
	except:
		return None



async def search_youtube_music_track(artist: str, track: str):
	try:
		tracks_data = []
		search_results = ytmusic.search(f'{artist} {track}', filter = 'songs')
		for result in search_results:
			if result['resultType'] == 'song':
				url = str(f'https://music.youtube.com/watch?v={result['videoId']}')
				identifier = str(result['videoId'])
				artists = []
				for names in result['artists']:
					artists.append(str(names['name']))
				title = str(result['title'])
				cover = str(result['thumbnails'][1]['url'])
				tracks_data.append({
					'url': url,
					'id': identifier,
					'artists': artists,
					'track': title,
					'cover': cover,
				})
		return filter_track(artist, track, tracks_data)
	except:
		return None



async def search_youtube_music_album(artist: str, album: str):
	try:
		result = ytmusic.search(f'{artist} {album}')[0]
		url = str(f'https://music.youtube.com/playlist?list={result['playlistId']}')
		if result['resultType'] == 'album':
			identifier = str(result['playlistId'])
			artists = []
			for names in result['artists']:
				artists.append(str(names['name']))
			title = str(result['title'])
			cover = str(result['thumbnails'][1]['url'])
			return {
				'url': url,
				'id': identifier,
				'artists': artists,
				'album': title,
				'cover': cover,
			}
		else:
			return None
	except:
		return None
