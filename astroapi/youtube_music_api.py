from ytmusicapi import YTMusic

ytmusic = YTMusic()

def search_youtube_music_track(artist, track):
    search_results = ytmusic.search(f'{artist} {track}',filter='songs')[0]
    try:
        return {
            'url': f'https://music.youtube.com/watch?v={search_results['videoId']}',
            'id': search_results['videoId'],
            'artist_name': search_results['artists'][0]['name'],
            'track_name': search_results['title'],
        }
    except:
        return {
            'url': '',
            'id': '',
            'artist_name': '',
            'track_name': '',
        }

def search_youtube_music_album(artist, album):
    search_results = ytmusic.get_album(ytmusic.search(f'{artist} {album}',filter='albums')[0]['browseId']) 
    try:
        return {
            'url': f'https://music.youtube.com/playlist?list={search_results['audioPlaylistId']}',
            'id': search_results['audioPlaylistId'],
            'artist_name': search_results['artists'][0]['name'],
            'album_name': search_results['title'],
        }
    except:
        return {
            'url': '',
            'id': '',
            'artist_name': '',
            'album_name': '',
        }
