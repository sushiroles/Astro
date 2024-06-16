import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

config = configparser.ConfigParser()
config.read('tokens.ini')

def search_spotify_track(artist: str, track: str):
	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	search_query = f'artist:{artist} track:{track}'
	search_results = sp.search(q=search_query, type='track')

	if search_results['tracks']['items']:
		track_info = search_results['tracks']['items'][0]
		artist_info = track_info['artists'][0]

		return {
			'url': track_info['external_urls']['spotify'],
			'id': track_info['id'],
			'artist_name': artist_info['name'],
			'track_name': track_info['name'],
			'cover_art': track_info['album']['images'][0]['url'],
		}  
	else:
		return None
  
def search_spotify_album(artist: str, album: str):
	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	search_query = f'artist:{artist} album:{album}'
	search_results = sp.search(q=search_query, type='album')

	if search_results['albums']['items']:
		album_info = search_results['albums']['items'][0]
		artist_info = album_info['artists'][0]
		return {
			'url': album_info['external_urls']['spotify'],
			'id': album_info['id'],
			'artist_name': artist_info['name'],
			'album_name': album_info['name'],
			'cover_art': album_info['images'][0]['url'],
		}  
	else:
		return None

def get_spotify_track(identifier: str):
	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	track = sp.track(identifier)
	return {
		'url': track['external_urls']['spotify'],
		'id': track['id'],
		'artist_name': track['artists'][0]['name'],
		'track_name': track['name'],
		'cover_art': track['album']['images'][0]['url'],
	}

def get_spotify_album(identifier: str):
	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	album = sp.album(identifier)
	return {
		'url': album['external_urls']['spotify'],
		'id': album['id'],
		'artist_name': album['artists'][0]['name'],
		'album_name': album['name'],
		'cover_art': album['images'][0]['url'],
	}

