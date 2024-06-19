
from spotify_nebula import *
#from apple_music_api import *
from youtube_music_nebula import *
from deezer_nebula import *
from tidal_nebula import *
from bandcamp_nebula import *

from etc import *


artist = 'beyonce'
album = 'cowboy carter'

start_time = current_time_ms()
print(search_spotify_album(artist,album))
print('\n')
print(search_youtube_music_album(artist,album))
print('\n')
print(search_deezer_album(artist,album))
print('\n')
print(search_tidal_album(artist,album))
print('\n')
print(search_bandcamp_album(artist,album))
print(f'this took {current_time_ms()-start_time}ms to run\n')


artist = 'beyonce'
track = 'im that girl'

start_time = current_time_ms()
print(search_spotify_track(artist,track))
print('\n')
print(search_youtube_music_track(artist,track))
print('\n')
print(search_deezer_track(artist,track))
print('\n')
print(search_tidal_track(artist,track))
print('\n')
print(search_bandcamp_track(artist,track))
print(f'this took {current_time_ms()-start_time}ms to run')
