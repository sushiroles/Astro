import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
try:
	from nebula_api.etc import *
	from nebula_api.filter import *
except:
	from etc import *
	from filter import *

config = configparser.ConfigParser()
config.read('tokens.ini')



def search_spotify_track(artist: str, track: str):
	tracks_data = []

	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	search_query = f'artist:{artist} track:{track}'
	search_results = sp.search(q = search_query, type = 'track', limit = 10)

	if search_results['tracks']['items']:
		for result in search_results['tracks']['items']:
			tracks_data.append({
				'url': str(result['external_urls']['spotify']),
				'id': str(result['id']),
				'id': str(result['id']),
				'artist_name': str(result['artists'][0]['name']),
				'track_name': str(result['name']),
				'cover_art': str(result['album']['images'][0]['url']),
			})
		return filter_track(artist, track, tracks_data)
	else:
		return None
  


def search_spotify_album(artist: str, album: str):
	albums_data = []

	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	search_query = f'artist:{artist} album:{album}'
	search_results = sp.search(q=search_query, type='album', limit = 10)

	if search_results['albums']['items']:
		for result in search_results['albums']['items']:
			albums_data.append({
				'url': str(result['external_urls']['spotify']),
				'id': str(result['id']),
				'artist_name': str(result['artists'][0]['name']),
				'album_name': str(result['name']),
				'release_year': str(result['release_date'][:4]),
				'cover_art': str(result['images'][0]['url']),
			})
		return filter_album(artist, album, albums_data)
	else:
		return None
