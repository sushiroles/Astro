from ytmusicapi import YTMusic
import configparser
import json
from etc import *

config = configparser.ConfigParser()
config.read('tokens.ini')


ytmusic = YTMusic({
    "scope": config['youtube_music']['scope'],
    "token_type": config['youtube_music']['token_type'],
    "access_token": config['youtube_music']['access_token'],
    "refresh_token": config['youtube_music']['refresh_token'],
    "expires_at": int(config['youtube_music']['expires_at']),
    "expires_in": int(config['youtube_music']['expires_in']),
})

def search_youtube_music_track(artist, track):
    try:
        tracks_data = []
        search_results = ytmusic.search(f'{artist} {track}', filter = 'songs', limit = 3)[:3]
        for search_results_num in range(len(search_results)):
            tracks_data.append({
                'url': f'https://music.youtube.com/watch?v={search_results[search_results_num]['videoId']}',
                'id': search_results[search_results_num]['videoId'],
                'artist_name': search_results[search_results_num]['artists'][0]['name'],
                'track_name': search_results[search_results_num]['title'],
                'cover_art': search_results[search_results_num]['thumbnails'][1]['url'],
            })
        return tracks_data
    except:
        return None

def search_youtube_music_album(artist, album):
    try:
        albums_data = []
        search = ytmusic.search(f'{artist} {album}', filter = 'albums', limit = 3)[:3]
        return search
        for search_results_num in range(len(search)):
            search_results = ytmusic.get_album(search[search_results_num]['browseId'])
            albums_data.append({
                'url': f'https://music.youtube.com/playlist?list={search_results['audioPlaylistId']}',
                'id': search_results['audioPlaylistId'],
                'artist_name': search_results['artists'][0]['name'],
                'album_name': search_results['title'],
                'cover_art': search_results['thumbnails'][1]['url'],
            })
        return albums_data
    except:
        return None

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(search_youtube_music_album('tyler the creator','call me if you get lost'), f, ensure_ascii=False, indent=4)