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
		artist_name = artist_info['name']
		track_name = track_info['name']
		url = track_info['external_urls']['spotify']
		identifier = track_info['id']
		cover_art = track_info['album']['images'][0]['url']
		return {
			'url': url,
			'id': identifier,
			'artist_name': artist_name,
			'track_name': track_name,
			'cover_art': cover_art,
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
		album_name = album_info['name']
		artist_info = album_info['artists'][0]
		artist_name = artist_info['name']
		url = album_info['external_urls']['spotify']
		cover_art = album_info['images'][0]['url']
		identifier = album_info['id']
		return {
			'url': url,
			'id': identifier,
			'artist_name': artist_name,
			'album_name': album_name,
			'cover_art': cover_art,
		}  
	else:
		return None
