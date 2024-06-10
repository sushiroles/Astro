from astroapi.spotify_api import *
#from astroapi.apple_music_api import *
from astroapi.youtube_music_api import *
from astroapi.deezer_api import *
#from astroapi.tidal_api import *
#from astroapi.amazon_music_api import *
#from astroapi.soundcloud_api import *
#from astroapi.bandcamp_api import *

# ignore this :3
#value=f'<:spotify:1247554944916000839> [Spotify]({search_result['spotify_url']})\n<:applemusic:1247554938733854761> Apple Music\n<:youtubemusic:1247554947696955464> YouTube Music\n<:deezer:1247554941724397649> [Deezer]({search_result['deezer_url']})\n<:tidal:1247554946123960362> Tidal\n<:amazonmusic:1247554937320112239> Amazon Music\n<:soundcloud:1247554943347327036> SoundCloud\n<:bandcamp:1247554940071841803> BandCamp',

def get_track_data(api_call: callable, contains_cover_art: bool):
    cover_art = ''
    try:
        call_results = api_call
        url = call_results['url']
        identifier = call_results['id']
        artist = call_results['artist_name']
        track = call_results['track_name']
        if contains_cover_art:
            cover_art = call_results['cover_art']
        check_data = {'artist_name': artist, 'track_name': track}
    except:
        url = ''
        identifier = ''
        artist = ''
        track = ''
        cover_art = ''
        check_data = {'artist_name': '', 'track_name': ''}
    return {
        'url': url,
        'id': identifier,
        'artist': artist,
        'track': track,
        'cover_art': cover_art,
        'check_data': check_data,
    }

def get_album_data(api_call: callable, contains_cover_art: bool):
    cover_art = ''
    try:
        call_results = api_call
        url = call_results['url']
        identifier = call_results['id']
        artist = call_results['artist_name']
        album = call_results['album_name']
        if contains_cover_art:
            cover_art = call_results['cover_art']
        check_data = {'artist_name': artist, 'album_name': album}
    except:
        url = ''
        identifier = ''
        artist = ''
        album = ''
        cover_art = ''
        check_data = {'artist_name': '', 'album_name': ''}
    return {
        'url': url,
        'id': identifier,
        'artist': artist,
        'album': album,
        'cover_art': cover_art,
        'check_data': check_data,
    }



def search_track(artist: str, track: str):
    artist_name = ''
    track_name = ''
    cover_art = ''
    requested_artist = artist
    requested_track = track


    # Search on Spotify
    spotify_data = get_track_data(search_spotify_track(artist.replace(''',''),track.replace(''','')),True)
    spotify_url = spotify_data['url']
    spotify_id = spotify_data['id']
    spotify_artist = spotify_data['artist']
    spotify_track = spotify_data['track']
    spotify_cover_art = spotify_data['cover_art']
    spotify_anchor = f'<:spotify:1247554944916000839> [Spotify]({spotify_url})\n'
    if artist_name == '' and track_name == '': 
        artist_name = spotify_artist
        track_name = spotify_track

    # Search on Apple Music
    #apple_music_data = get_track_data(search_apple_music_track(artist.replace(''',''),track.replace(''','')),False)
    #apple_music_url = apple_music_data['url']
    #apple_music_id = apple_music_data['id']
    #apple_music_artist = apple_music_data['artist']
    #apple_music_track = apple_music_data['track']
    #apple_music_anchor = f'<:applemusic:1247554938733854761> [Apple Music]({apple_music_url})\n'
    #apple_music_check_data = apple_music_data['check_data']
    #if artist_name == '' and track_name == '': 
    #    artist_name = apple_music_artist
    #    track_name = apple_music_track

    # Search on YouTube Music
    youtube_music_data = get_track_data(search_youtube_music_track(artist.replace(''',''),track.replace(''','')),False)
    youtube_music_url = youtube_music_data['url']
    youtube_music_id = youtube_music_data['id']
    youtube_music_artist = youtube_music_data['artist']
    youtube_music_track = youtube_music_data['track']
    youtube_music_anchor = f'<:youtubemusic:1247554947696955464> [YouTube Music]({youtube_music_url})\n'
    if artist_name == '' and track_name == '': 
        artist_name = youtube_music_artist
        track_name = youtube_music_track

    # Search on Deezer
    deezer_data = get_track_data(search_deezer_track(spotify_artist,spotify_track),True)
    deezer_url = deezer_data['url']
    deezer_id = deezer_data['id']
    deezer_artist = deezer_data['artist']
    deezer_track = deezer_data['track']
    deezer_cover_art = deezer_data['cover_art']
    deezer_anchor = f'<:deezer:1247554941724397649> [Deezer]({deezer_url})\n'
    if artist_name == '' and track_name == '': 
        artist_name = deezer_artist
        track_name = deezer_track

    cover_art = deezer_cover_art
    service_anchor = f'{spotify_anchor}{youtube_music_anchor}{deezer_anchor}'

    return{
        'cover_art': cover_art,
        'artist_name': artist_name,
        'track_name': track_name,
        'service_anchor': service_anchor,

        'requested_artist': requested_artist,
        'requested_track': requested_track,

        'spotify_url': spotify_url,
        'spotify_id': spotify_id,

        #'apple_music_url': apple_music_url,
        #'apple_music_id': apple_music_id,

        'youtube_music_url': youtube_music_url,
        'youtube_music_id': youtube_music_id,

        'deezer_url': deezer_url,
        'deezer_id': deezer_id,
    }

def search_album(artist: str, album: str):
    artist_name = ''
    album_name = ''
    cover_art = ''
    requested_artist = artist
    requested_album = album


    # Search on Spotify
    spotify_data = get_album_data(search_spotify_album(artist.replace(''',''),album.replace(''','')),False)
    spotify_url = spotify_data['url']
    spotify_id = spotify_data['id']
    spotify_artist = spotify_data['artist']
    spotify_album = spotify_data['album']
    spotify_cover_art = spotify_data['cover_art']
    if spotify_url != '':
        spotify_anchor = f'<:spotify:1247554944916000839> [Spotify]({spotify_url})\n'
    else:
        spotify_anchor = ''
    if artist_name == '' and album_name == '': 
        artist_name = spotify_artist
        album_name = spotify_album


    # Search on Apple Music
    #apple_music_data = get_album_data(search_apple_music_album(artist.replace(''',''),album.replace(''','')),False)
    #apple_music_url = apple_music_data['url']
    #apple_music_id = apple_music_data['id']
    #apple_music_artist = apple_music_data['artist']
    #apple_music_album = apple_music_data['album']
    #apple_music_anchor = f'<:applemusic:1247554938733854761> [Apple Music]({apple_music_url})\n'
    #if artist_name == '' and album_name == '': 
    #    artist_name = apple_music_artist
    #    album_name = apple_music_album

    # Search on YouTube Music
    youtube_music_data = get_album_data(search_youtube_music_album(artist.replace(''',''),album.replace(''','')),False)
    youtube_music_url = youtube_music_data['url']
    youtube_music_id = youtube_music_data['id']
    youtube_music_artist = youtube_music_data['artist']
    youtube_music_album = youtube_music_data['album']
    if youtube_music_url != '':
        youtube_music_anchor = f'<:youtubemusic:1247554947696955464> [YouTube Music]({youtube_music_url})\n'
    else:
        youtube_music_anchor = ''
    if artist_name == '' and album_name == '': 
        artist_name = youtube_music_artist
        album_name = youtube_music_album

    # Search on Deezer
    deezer_data = get_album_data(search_deezer_album(spotify_artist,spotify_album),True)
    deezer_url = deezer_data['url']
    deezer_id = deezer_data['id']
    deezer_artist = deezer_data['artist']
    deezer_album = deezer_data['album']
    deezer_cover_art = deezer_data['cover_art']
    if deezer_url != '':
        deezer_anchor = f'<:deezer:1247554941724397649> [Deezer]({deezer_url})\n'
    else:
        deezer_anchor = ''
    if artist_name == '' and album_name == '': 
        artist_name = deezer_artist
        album_name = deezer_album

    cover_art = deezer_cover_art
    service_anchor = f'{spotify_anchor}{youtube_music_anchor}{deezer_anchor}'

    return{
        'cover_art': cover_art,
        'artist_name': artist_name,
        'album_name': album_name,
        'service_anchor': service_anchor,

        'requested_artist': requested_artist,
        'requested_album': requested_album,

        'spotify_url': spotify_url,
        'spotify_id': spotify_id,

        #'apple_music_url': apple_music_url,
        #'apple_music_id': apple_music_id,

        'youtube_music_url': youtube_music_url,
        'youtube_music_id': youtube_music_id,

        'deezer_url': deezer_url,
        'deezer_id': deezer_id,
    }
