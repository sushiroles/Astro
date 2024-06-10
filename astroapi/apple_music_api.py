import urllib.request, json 



def search_apple_music_track(artist, track):
    query_artist = artist.replace(' ','-').lower()
    query_track = track.replace(' ','-').lower()
    bare_artist = artist.replace(',','').lower()
    bare_track = track.replace(',','').lower()
    base_url = 'https://itunes.apple.com/search?'
    url_params = {
        'term': f'{query_artist}-{query_track}',
        'media': 'music'
    }
    with urllib.request.urlopen(base_url + '&'.join(f'{key}={value}' for key, value in url_params.items())) as url:
        data = json.load(url)
        for i in range(data['resultCount']):
            if data['results'][i]['artistName'].lower().find(bare_artist) >=0 and data['results'][i]['trackName'].lower().find(bare_track) >= 0 == False:
                return {
                    'url': data['results'][i]['trackViewUrl'],
                    'id': data['results'][i]['trackId'],
                    'artist_name': data['results'][i]['artistName'],
                    'track_name': data['results'][i]['trackName'],
                }
        return None

def search_apple_music_album(artist, album):
    query_artist = artist.replace(' ','-').lower()
    query_album = album.replace(' ','-').lower()
    bare_artist = artist.replace(',','').lower()
    bare_album = album.replace(',','').lower()
    base_url = 'https://itunes.apple.com/search?'
    url_params = {
        'term': f'{query_artist}-{query_album}',
        'media': 'music'
    }
    with urllib.request.urlopen(base_url + '&'.join(f'{key}={value}' for key, value in url_params.items())) as url:
        data = json.load(url)
        print(f'{base_url + '&'.join(f'{key}={value}' for key, value in url_params.items())}')
        for i in range(data['resultCount']):
            link = f'https://music.apple.com/album/{data['results'][i]['collectionName']}/{data['results'][i]['collectionId']}'
            if data['results'][i]['artistName'].lower().find(bare_artist) >=0 and data['results'][i]['collectionName'].lower().find(bare_album) >= 0 == False:
                return {
                    'url': link,
                    'id': data['results'][i]['collectionId'],
                    'artist_name': data['results'][i]['artistName'],
                    'album_name': data['results'][i]['collectionName'],
                }
        return None
