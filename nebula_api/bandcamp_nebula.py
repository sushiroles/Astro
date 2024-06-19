from bandcamp_api import Bandcamp
from etc import *

bc = Bandcamp()

def search_bandcamp_track(artist: str, track: str):
    try:
        tracks_data = []
        search_results = bc.search(f'{artist} {track}')[:5]
        for search_results_num in range(len(search_results)):
            try:
                tracks_data.append({
                    'url': search_results[search_results_num].track_url,
                    'id': '',
                    'artist_name': search_results[search_results_num].artist_title,
                    'track_name': search_results[search_results_num].track_title,
                    'cover_art': '',
                })
            except:
                pass
        return tracks_data
    except:
        return None

def search_bandcamp_album(artist: str, album: str):
    try:
        albums_data = []
        search_results = bc.search(f'{artist} {album}')[:5]
        for search_results_num in range(len(search_results)):
            try:
                albums_data.append({
                    'url': search_results[search_results_num].album_url,
                    'id': '',
                    'artist_name': search_results[search_results_num].artist_title,
                    'album_name': search_results[search_results_num].album_title,
                    'cover_art': '',
                })
            except:
                pass
        return albums_data
    except Exception as e:
        return e
