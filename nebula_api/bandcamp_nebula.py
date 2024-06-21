from bandcamp_api import Bandcamp
from datetime import *
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *

bc = Bandcamp()



def search_bandcamp_track(artist: str, track: str):
    try:
        tracks_data = []
        search_results = bc.search(f'{artist} {track}')[:10]
        for result in search_results:
            if result.type == 'track':
                tracks_data.append({
                    'url': str(result.track_url),
                    'id': str(result.track_id),
                    'artist_name': str(result.artist_title),
                    'track_name': str(result.track_title),
                    'cover_art': str(result.image_url),
                })
        return filter_track(artist, track, tracks_data)
    except:
        return None



def search_bandcamp_album(artist: str, album: str):
        try:
            albums_data = []
            search_results = bc.search(f'{artist} {album}')
            for result in search_results:
                if result.type == 'album':
                    albums_data.append({
                        'url': str(result.album_url),
                        'id': str(result.album_id),
                        'artist_name': str(result.artist_title),
                        'album_name': str(result.album_title),
                        'release_year': '', # fuck you
                        'cover_art': str(result.image_url),
                    })
            return filter_album(artist, album, albums_data)
        except:
            return None

