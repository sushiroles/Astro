from ytmusicapi import YTMusic
import json
from nebula_api.milkyway import *

ytmusic = YTMusic()

def search_youtube_music_track(artist, track):
    try:
        search_results = ytmusic.search(f'{artist} {track}',filter='songs')[0]
        return {
            'url': f'https://music.youtube.com/watch?v={search_results['videoId']}',
            'id': search_results['videoId'],
            'artist_name': search_results['artists'][0]['name'],
            'track_name': search_results['title'],
            'cover_art': search_results['thumbnails'][1]['url'],
        }
    except Exception as error:
        log('ERROR', f'Inside search_youtube_music_track(): "{error}" --- artist: {artist} / track: {track}')
        return None

def search_youtube_music_album(artist, album):
    try:
        search_results = ytmusic.get_album(ytmusic.search(f'{artist} {album}',filter='albums')[0]['browseId']) 
        return {
            'url': f'https://music.youtube.com/playlist?list={search_results['audioPlaylistId']}',
            'id': search_results['audioPlaylistId'],
            'artist_name': search_results['artists'][0]['name'],
            'album_name': search_results['title'],
            'cover_art': search_results['thumbnails'][1]['url'],
        }
    except Exception as error:
        log('ERROR', f'Inside search_youtube_music_album(): "{error}" --- artist: {artist} / album: {album}')
        return None
