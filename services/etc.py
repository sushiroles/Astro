from datetime import *
from time import time
from unidecode import *
from urllib.parse import urlparse
from urllib import request
import json
import re
import discord as discord
from PIL import Image
import requests
from io import BytesIO
import numpy as np



def log(type: str, message: str, parameters: str = None, anchors: str = None):
	embed = discord.Embed(
		title = f'{type}',
		colour = 0x0097f5,
	)
		
	embed.add_field(
		name = 'Message',
		value = f'{message}',
		inline = False
	)

	if parameters != None:
		embed.add_field(
			name = 'Parameters',
			value = f'{parameters}',
			inline = False
		)

	if anchors != None:
		embed.add_field(
			name = 'Anchors',
			value = f'{anchors}',
			inline = False
		)

	return embed

def current_time():
	return int(time())

def current_time_ms():
	return int(time() * 1000)

def save_json(json_data: dict):
	with open('save_json_data.json', 'w', encoding = 'utf-8') as f:
		json.dump(json_data, f, ensure_ascii = False, indent = 4)

def remove_punctuation(string: str, remove_all: bool):
	all_punc = f'''!()[];:'",<>./?@#$%^&*`_~'''
	some_punc = f'''!()[];:'",<>./?^*_~`'''
	for element in string:
		if remove_all == True:
			if element in all_punc:
				string = string.replace(element, '')
		elif remove_all == False:
			if element in some_punc:
				string = string.replace(element, '')
	return string

def replace_punctuation_with_spaces(string: str):
	punc = f'''!()[];:'",<>./?^*_`-~'''
	for element in string:
		if element in punc:
			string = string.replace(element, ' ')
	return string

def replace_with_ascii(string: str):
	return unidecode(string)

def bare_bones(string: str, remove_all_punctuation: bool = True):
	return replace_with_ascii(remove_punctuation(string, remove_all_punctuation)).lower().replace('  ',' ')

def split_artists(string: str):
	strings = re.split(r",|\&", string)
	fixed_strings = []
	for element in strings:
		if element == ' ':
			continue
		if element[0] == ' ':
			element = element[1:]
		if element[-1] == ' ':
			element = element[:-1]
		fixed_strings.append(element)
	return fixed_strings

def get_common_data(data: list):
	element_counts = {}
	for element in data:
		if element in element_counts:
			element_counts[element] += 1
		else:
			element_counts[element] = 1
 
	max_count = max(element_counts.values(), default=0)

	most_common = [key for key, value in element_counts.items() if value == max_count]

	return most_common[0] if most_common else None

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

def get_average_color(image_url: str, quality: int = 5):
	try:
		response = requests.get(image_url)
		image = Image.open(BytesIO(response.content))
	except:
		return 0xf5c000

	width, height = image.size
	new_width = width // quality
	new_height = height // quality
	image = image.resize((new_width, new_height))

	pixels = image.convert('RGB').getdata()
	average_color = np.mean(pixels, axis = 0).astype(int)

	hex_color = "#{:02x}{:02x}{:02x}".format(*average_color)
	return int(hex_color[1:], base = 16)

def remove_feat(string: str):
	if string.lower().find('feat. ') >= 0:
		if string[string.lower().index('feat. ')-1] == '[':
			first_bracket = string.lower().index('feat. ')-1
			second_bracket = string.lower().index('feat. ')-1
			while string[second_bracket] != ']':
				second_bracket += 1
			string = string.replace(string[first_bracket:second_bracket],'')
		elif string[string.lower().index('feat. ')-1] == '(':
			first_bracket = string.lower().index('feat. ')-1
			second_bracket = string.lower().index('feat. ')-1
			while string[second_bracket] != ')':
				second_bracket += 1
			string = string.replace(string[first_bracket:second_bracket],'')
		elif string[string.lower().index('feat. ')-1] == ' ':
			string = string[:string.lower().index('feat. ')-1]
	if string.lower().find('(with ') >= 0 or string.lower().find('[with ') >= 0:
		if string[string.lower().index('with ')-1] == '[':
			first_bracket = string.lower().index('with ')-1
			second_bracket = string.lower().index('with ')-1
			while string[second_bracket] != ']':
				second_bracket += 1
			string = string.replace(string[first_bracket:second_bracket],'')
		elif string[string.lower().index('with ')-1] == '(':
			first_bracket = string.lower().index('with ')-1
			second_bracket = string.lower().index('with ')-1
			while string[second_bracket] != ')':
				second_bracket += 1
			string = string.replace(string[first_bracket:second_bracket],'')
	return string

def optimize_string(string: str):
	string = remove_feat(string)
	string = replace_punctuation_with_spaces(string)
	string = bare_bones(string, False)
	string_list = string.split(sep = ' ')
	for counter in range(string_list.count('')):
		string_list.remove('')
	return string_list

async def check_reaction(message, reaction_emoji):
	if not message.reactions:
		return False
	for reaction in message.reactions:
		if reaction.emoji == reaction_emoji:
			return True
	return False

async def add_reactions(message, emojis: list):
	for emoji in emojis:
		await message.add_reaction(emoji)
