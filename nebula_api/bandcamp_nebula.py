from bandcamp_api import Bandcamp
from nebula_api.log import *

bc = Bandcamp()

def search_bandcamp_track(artist: str, track: str):
    try:
        search = bc.search(f'{artist} {track}')
        counter = 0
        while search[counter].artist_title != artist:
            counter += 1
        return {
            'url': search[counter].track_url,
			'id': '',
			'artist_name': search[counter].artist_title,
			'track_name': search[counter].track_title,
			'cover_art': '',
        }
    except Exception as error:
        log('ERROR', f'Inside search_bandcamp_track(): "{error}" --- artist: {artist} / track: {track}')
        return None

def search_bandcamp_album(artist: str, album: str):
    try:
        search = bc.search(f'{artist} {album}')
        counter = 0
        while search[counter].artist_title != artist:
            counter += 1
        return {
            'url': search[counter].album_url,
			'id':  '',
			'artist_name': search[counter].artist_title,
			'album_name': search[counter].album_title,
			'cover_art': '',
        }
    except Exception as error:
        log('ERROR', f'Inside search_bandcamp_album(): "{error}" --- artist: {artist} / album: {album}')
        return None