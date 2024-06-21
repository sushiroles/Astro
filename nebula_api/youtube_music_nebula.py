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
        search_results = ytmusic.search(f'{artist} {track}', filter = 'songs')[:10]
        for result in search_results:
            tracks_data.append({
                'url': str(f'https://music.youtube.com/watch?v={result['videoId']}'),
                'id': str(result['videoId']),
                'artist_name': str(result['artists'][0]['name']),
                'track_name': str(result['title']),
                'cover_art': str(result['thumbnails'][1]['url']),
            })
        return filter_track(artist, track, tracks_data)
    except:
        return None



def search_youtube_music_album(artist, album):
    try:
        albums_data = []
        search = ytmusic.search(f'{artist} {album}', filter = 'albums')[:10]
        for data in search:
            albums_data.append({
                'artist_name': str(data['artists'][0]['name']),
                'album_name': str(data['title']),
                'browse_id': str(data['browseId'])
            })
        browse_id = filter_album(artist, album, albums_data)['browse_id']
        album_search_data = ytmusic.get_album(browse_id)
        album_data = {
            'url': str(f'https://music.youtube.com/playlist?list={album_search_data['audioPlaylistId']}'),
			'id': str(album_search_data['audioPlaylistId']),
			'artist_name': str(album_search_data['artists'][0]['name']),
			'album_name': str(album_search_data['title']),
			'release_year': str(album_search_data['year']),
			'cover_art': str(album_search_data['thumbnails'][3]['url']),
        }
        return album_data
    except:
        return None
