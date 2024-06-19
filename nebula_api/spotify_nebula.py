import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

config = configparser.ConfigParser()
config.read('tokens.ini')

def search_spotify_track(artist: str, track: str):
	tracks_data = []

	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	search_query = f'artist:{artist} track:{track}'
	search_results = sp.search(q = search_query, type = 'track', limit = 5)

	if search_results['tracks']['items']:
		for search_results_num in range(len(search_results['tracks']['items'])):
			track_info = search_results['tracks']['items'][search_results_num]
			artist_info = track_info['artists'][0]
			tracks_data.append({
				'url': track_info['external_urls']['spotify'],
				'id': track_info['id'],
				'artist_name': artist_info['name'],
				'track_name': track_info['name'],
				'cover_art': track_info['album']['images'][0]['url'],
			})
		return tracks_data
	else:
		return None
  
def search_spotify_album(artist: str, album: str):
	albums_data = []

	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	search_query = f'artist:{artist} album:{album}'
	search_results = sp.search(q=search_query, type='album', limit = 5)

	if search_results['albums']['items']:
		for search_results_num in range(len(search_results['albums']['items'])):
			album_info = search_results['albums']['items'][search_results_num]
			artist_info = album_info['artists'][0]
			albums_data.append({
				'url': album_info['external_urls']['spotify'],
				'id': album_info['id'],
				'artist_name': artist_info['name'],
				'album_name': album_info['name'],
				'cover_art': album_info['images'][0]['url'],
			})
		return albums_data
	else:
		return None
