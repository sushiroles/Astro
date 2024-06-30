from ytmusicapi import YTMusic
import configparser
import json
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *

ytmusic = YTMusic()



def search_youtube_music_track(artist, track):
	try:
		tracks_data = []
		search_results = ytmusic.search(f'{artist} {track}', filter = 'songs')
		for result in search_results:
			url = str(f'https://music.youtube.com/watch?v={result['videoId']}')
			identifier = str(result['videoId'])
			artists = []
			for names in result['artists']:
				artists.append(str(names['name']))
			title = str(result['title'])
			year = '' # fuck you
			cover = str(result['thumbnails'][1]['url'])
			tracks_data.append({
				'url': url,
				'id': identifier,
				'artists': artists,
				'track': title,
				'year': year,
				'cover': cover,
			})
		return filter_track(artist, track, tracks_data)
	except:
		return None



def search_youtube_music_album(artist, album):
	try:
		albums_data = []
		search = ytmusic.search(f'{artist} {album}', filter = 'albums')
		for data in search:
			artists = []
			for names in data['artists']:
				artists.append(str(names['name']))
			title = str(data['title'])
			browse_id = str(data['browseId'])
			albums_data.append({
				'artists': artists,
				'album': title,
				'browse_id': browse_id,
			})
		album_search_data = ytmusic.get_album(filter_album(artist, album, albums_data)['browse_id'])
		url = str(f'https://music.youtube.com/playlist?list={album_search_data['audioPlaylistId']}')
		identifier = str(album_search_data['audioPlaylistId'])
		artists = []
		for names in album_search_data['artists']:
			artists.append(names['name'])
		title = str(album_search_data['title'])
		year = str(album_search_data['year'])
		cover = str(album_search_data['thumbnails'][3]['url'])
		album_data = {
			'url': url,
			'id': identifier,
			'artists': artists,
			'album': title,
			'year': year,
			'cover': cover,
		}
		return album_data
	except:
		return None
