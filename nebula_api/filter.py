try:
	from nebula_api.etc import *
except:
	from etc import *

def filter_track(artist: str, track: str, tracks_data: list):
    artist = remove_punctuation(artist).lower()
    track = remove_punctuation(track).lower()
    for data in tracks_data:
        data_artist = remove_punctuation(data['artist_name']).lower()
        data_track = remove_punctuation(data['track_name']).lower()
        if data_artist.find(artist) >= 0 and data_track.find(track) >= 0:
            return data
    return None

def filter_album(artist: str, album: str, albums_data: list):
    artist = remove_punctuation(artist).lower()
    album = remove_punctuation(album).lower()
    for data in albums_data:
        data_artist = remove_punctuation(data['artist_name']).lower()
        data_album = remove_punctuation(data['album_name']).lower()
        if data_artist.find(artist) >= 0 and data_album.find(album) >= 0:
            return data
    return None