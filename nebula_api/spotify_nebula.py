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
	search_results = sp.search(q = search_query, type = 'track')

	if search_results['tracks']['items']:
		for result in search_results['tracks']['items']:
			url = str(result['external_urls']['spotify'])
			identifier = str(result['id'])
			artists = []
			for names in result['artists']:
				artists.append(str(names['name']))
			title = str(result['name'])
			year = str(result['album']['release_date'][:4])
			cover = str(result['album']['images'][0]['url'])
			tracks_data.append({
				'url': url,
				'id': identifier,
				'artists': artists,
				'track': title,
				'year': year,
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
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	search_query = f'artist:{artist} album:{album}'
	search_results = sp.search(q=search_query, type='album')

	if search_results['albums']['items']:
		for result in search_results['albums']['items']:
			url = str(result['external_urls']['spotify'])
			identifier = str(result['id'])
			artists = []
			for names in result['artists']:
				artists.append(str(names['name']))
			title = str(result['name'])
			year = str(result['release_date'][:4])
			cover = str(result['images'][0]['url'])
			albums_data.append({
				'url': url,
				'id': identifier,
				'artists': artists,
				'album': title,
				'year': year,
				'cover': cover,
			})
		return filter_album(artist, album, albums_data)
	else:
		return None
