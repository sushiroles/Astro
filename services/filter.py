try:
	from services.etc import *
except:
	from etc import *



def filter_track(tracks_data: list, artist: str, track: str, collection: str = None, is_explicit: bool = None):
	max_score = 2000
	if collection != None:
		max_score += 1000
	if is_explicit != None:
		max_score += 500

	data_with_similarity = []
	for data in tracks_data:
		track_similarity = 0

		artist_input = bare_bones(artist)
		artists_reference = data['artists']
		artists_with_similarity = []
		for artist_name in artists_reference:
			artists_with_similarity.append([calculate_similarity(bare_bones(artist_name), artist_input), artist_name])
		artists_with_similarity = sort_similarity_lists(artists_with_similarity)
		if artists_with_similarity != [] and artists_with_similarity[0][0] > 300:
			track_similarity += artists_with_similarity[0][0]
		else:
			continue

		title_input = bare_bones(track)
		title_reference = remove_feat(data['title'])
		track_similarity += calculate_similarity(bare_bones(title_reference), title_input)

		if collection != None:
			collection_input = bare_bones(collection)
			collection_reference = data['collection_name']
			track_similarity += calculate_similarity(bare_bones(collection_reference), collection_input)

		if is_explicit != None:
			if is_explicit == data['is_explicit']:
				track_similarity += 500

		data_with_similarity.append([track_similarity, data])
	
	data_with_similarity = sort_similarity_lists(data_with_similarity)
	if data_with_similarity != []:
		if percentage(max_score, data_with_similarity[0][0]) > 30:
			return data_with_similarity[0][1]
		else:
			return {
				'type': 'empty_response'
			}
	else:
		return {
			'type': 'empty_response'
		}



def filter_album(albums_data: list, artist: str, album: str, year: str = None):
	max_score = 2000
	if year != None:
		max_score += 1000

	data_with_similarity = []
	for data in albums_data:
		track_similarity = 0

		artist_input = bare_bones(artist)
		artists_reference = data['artists']
		artists_with_similarity = []
		for artist_name in artists_reference:
			artists_with_similarity.append([calculate_similarity(bare_bones(artist_name), artist_input), artist_name])
		artists_with_similarity = sort_similarity_lists(artists_with_similarity)
		if artists_with_similarity != [] and artists_with_similarity[0][0] > 300:
			track_similarity += artists_with_similarity[0][0]
		else:
			continue

		title_input = bare_bones(album)
		title_reference = remove_feat(data['title'])
		track_similarity += calculate_similarity(bare_bones(title_reference), title_input)

		if year != None:
			if year == data['year']:
				track_similarity += 1000

		data_with_similarity.append([track_similarity, data])
	
	data_with_similarity = sort_similarity_lists(data_with_similarity)
	if data_with_similarity != []:
		if percentage(max_score, data_with_similarity[0][0]) > 30:
			return data_with_similarity[0][1]
		else:
			return {
				'type': 'empty_response'
			}
	else:
		return {
			'type': 'empty_response'
		}
