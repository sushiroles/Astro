from datetime import *
from time import time
from unidecode import *
from urllib.parse import urlparse
from urllib import request
import json
import re
import discord as discord


def log(type: str, message: str, parameters: str):
	time = datetime.now()
	log_format = time.strftime(f'(%x - %X) [{type}] {message}\n')
	embed = discord.Embed(
		title = f'{type}',
		colour = 0x3f81eb,
	)
		
	embed.add_field(
		name = 'Message',
		value = f'{message}',
		inline = False
	)

	embed.add_field(
		name = 'Parameters',
		value = f'{parameters}',
		inline = False
	)

	return embed

def current_time_ms():
	return int(time() * 1000)

def save_json(json_data: dict):
	with open('save_json_data.json', 'w', encoding = 'utf-8') as f:
		json.dump(json_data, f, ensure_ascii = False, indent = 4)

def remove_punctuation(string: str):
	punc = f'''!()[];:'",<>./?@#$%^&*_~'''
	for element in string:
		if element in punc:
			string = string.replace(element, '')
	return string

def replace_with_ascii(string: str):
	return unidecode(string)

def bare_bones(string: str):
	return replace_with_ascii(remove_punctuation(string)).lower()

def split_artists(string: str):
	strings = re.split(r",|\&", string)
	fixed_strings = []
	for element in strings:
		if element[0] == ' ':
			element = element[1:]
		if element[-1] == ' ':
			element = element[:-1]
		fixed_strings.append(element)
	return fixed_strings

def get_common_data(data: list):
	element_counts = {}
	for element in data:
		if element in element_counts and element != '':
			element_counts[element] += 1
		else:
			element_counts[element] = 1
	max_count = max(element_counts.values())
	most_common = {key: value for key, value in element_counts.items() if value == max_count}
	return list(most_common.items())

def find_urls(string: str):
	words = string.split()
	urls = []
	for word in words:
		parsed = urlparse(word)
		if parsed.scheme and parsed.netloc:
			urls.append(word)
	return urls

def get_regular_url(deferred_url: str):
	try:
		data = request.urlopen(deferred_url)
	except:
		return None
	regular_url = data.geturl()
	return regular_url