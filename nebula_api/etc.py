from datetime import *
from time import time
from unidecode import *
import json
import re


def log(type: str, message: str):
	time = datetime.now()
	log_format = time.strftime(f'(%x - %X) [{type}] {message}\n')
	print(log_format)
	open('logs.txt','a').write(log_format)

def current_time_ms():
	return int(time() * 1000)

def save_json(json_data):
	with open('save_json_data.json', 'w', encoding = 'utf-8') as f:
		json.dump(json_data, f, ensure_ascii = False, indent = 4)

def remove_punctuation(string):
	punc = f'''!()-[];:'",<>./?@#$%^&*_~'''
	for element in string:
		if element in punc:
			string = string.replace(element, '')
	return string

def replace_with_ascii(string):
	return unidecode(string)

def bare_bones(string):
	return replace_with_ascii(remove_punctuation(string)).lower()

def split_artists(string):
	strings = re.split(r",|\&", string)
	fixed_strings = []
	for element in strings:
		if element[0] == ' ':
			element = element[1:]
		if element[-1] == ' ':
			element = element[:-1]
		fixed_strings.append(element)
	return fixed_strings