import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
try:
	from services.etc import *
	from services.filter import *
except:
	from etc import *
	from filter import *



config = configparser.ConfigParser()
config.read('tokens.ini')



def is_spotify_track(url: str):
	return bool(url.find('https://open.spotify.com/track/') >= 0)
	
def is_spotify_album(url: str):
	return bool(url.find('https://open.spotify.com/album/') >= 0)

def get_spotify_id(url: str):
	return url[31:53]



def search_spotify_track(artist: str, track: str):
	tracks_data = []

	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

	search_query = f'artist:{artist} track:{track}'
	search_results = sp.search(q = search_query, type = 'track')

	if search_results['tracks']['items']:
		for result in search_results['tracks']['items']:
			url = str(result['external_urls']['spotify'])
			identifier = str(result['id'])
			artists = []
			for names in result['artists']:
				artists.append(str(names['name']))
			title = str(result['name'])
			cover = str(result['album']['images'][0]['url'])
			tracks_data.append({
				'url': url,
				'id': identifier,
				'artists': artists,
				'track': title,
				'cover': cover,
			})
		return filter_track(artist, track, tracks_data)
	else:
		return None
  


def search_spotify_album(artist: str, album: str):
	albums_data = []

	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

	search_query = f'artist:{artist} album:{album}'
	search_results = sp.search(q = search_query, type = 'album')

	if search_results['albums']['items']:
		for result in search_results['albums']['items']:
			url = str(result['external_urls']['spotify'])
			identifier = str(result['id'])
			artists = []
			for names in result['artists']:
				artists.append(str(names['name']))
			title = str(result['name'])
			cover = str(result['images'][0]['url'])
			albums_data.append({
				'url': url,
				'id': identifier,
				'artists': artists,
				'album': title,
				'cover': cover,
			})
		return filter_album(artist, album, albums_data)
	else:
		return None



def get_spotify_track(identifier: str):
	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	track = sp.track(identifier)
	url = str(track['external_urls']['spotify'])
	identifier = str(track['id'])
	artists = []
	for names in track['artists']:
		artists.append(str(names['name']))
	title = str(track['name'])
	cover = str(track['album']['images'][0]['url'])
	return {
		'url': url,
		'id': identifier,
		'artists': artists,
		'track': title,
		'cover': cover,
	}



def get_spotify_album(identifier: str):
	spotify_id = config['spotify']['id']
	spotify_secret = config['spotify']['secret']
	client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	album = sp.album(identifier)
	url = str(album['external_urls']['spotify'])
	identifier = str(album['id'])
	artists = []
	for names in album['artists']:
		artists.append(str(names['name']))
	title = str(album['name'])
	cover = str(album['images'][0]['url'])
	return {
		'url': url,
		'id': identifier,
		'artists': artists,
		'album': title,
		'cover': cover,
	}
