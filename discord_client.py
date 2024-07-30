import discord as discord 
from discord import app_commands
from discord import Spotify
from discord.ext import tasks

import configparser
import asyncio
from random import randint
from time import sleep

from app_services import *



config = configparser.ConfigParser()
config.read('tokens.ini')



class Client(discord.Client): 
	def __init__(self):
		discordintents = discord.Intents.all()
		discordintents.message_content = True
		discordintents.presences = True
		discordintents.members = True
		super().__init__(intents = discordintents)		
		self.synced = False								
	async def on_ready(self): 
		await self.wait_until_ready() 		
		if not self.synced:					
			await tree.sync()
			self.synced = True
		discord_presence.start()



client = Client() 
tree = app_commands.CommandTree(client)
is_internal = True
presence_statuses = open('discord_presence.txt','r').readlines()



def success_embed(title: str, artists: list, cover: str, anchor: str):
	embed = discord.Embed(
		title = f'{title}',
		description = f'by {', '.join(artists)}',
		colour = get_average_color(cover),
	)
		
	embed.add_field(
		name = 'You can find it on:',
		value = anchor,
		inline = False
	)
	
	embed.set_thumbnail(url = cover)
	embed.set_footer(text = 'Thank you for using Astro!')

	return embed


def fail_embed(message: str):
	embed = discord.Embed(
		title = f'Oh no!',
		colour = 0xf5c000,
	)
		
	embed.add_field(
		name = '',
		value = message,
		inline = False
	)
	
	embed.set_footer(text = 'Thank you for using Astro!')

	return embed



@client.event
async def on_message(message):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	urls = find_urls(message.content)
	if urls != []:
		for url in urls:
			start_time = current_time_ms()

			try:
				music_data = await get_music_data(url)
				data = music_data['data']
				url_type = music_data['url_type']
				if data == None:
					await logs_channel.send(embed = log('FAILURE', f'Failed to get track data from URL', f'URL: {url}'))
					continue
				await message.add_reaction('❗')
			except Exception as error:
				await logs_channel.send(embed = log('ERROR', f'When getting track data from URL - "{error}"', f'URL: {url}'))
				continue

			while current_time_ms() - start_time <= 30000:
				try:
					if url_type == 'track':
						data['track'] = remove_feat(data['track'])
						search_result = await search_track_from_url_data(max(data['artists'], key = len), data['track'])
						title = search_result['track']
					elif url_type == 'album':
						search_result = await search_album_from_url_data(max(data['artists'], key = len), data['album'])
						title = search_result['album']
					break
				except Exception as error:
					await logs_channel.send(embed = log('NOTICE', f'Error when searching link - "{error}", retrying...', f'URL: {url}'))
					await asyncio.sleep(5)
			
			if current_time_ms() - start_time >= 30000:
				await message.add_reaction('⌛')
				await logs_channel.send(embed = log('FAILURE', f'Search timed out', f'URL: {url}'))
				if await check_reaction(message, '❗'):
					await message.remove_reaction('❗', client.user)
				continue

			if search_result['anchor'].count('\n') <= 1:
				await message.add_reaction('🤷')
				await logs_channel.send(embed = log('RETREAT', f'Insufficient results', f'URL: {url}'))
				if await check_reaction(message, '❗'):
					await message.remove_reaction('❗', client.user)
				continue
				
			if await check_reaction(message, '❗'):
				await message.remove_reaction('❗', client.user)

			embed = await message.reply(embed = success_embed(title, search_result['artists'], search_result['cover'], search_result['anchor']), mention_author = False)
			await add_reactions(embed, ['👍','👎'])
			await logs_channel.send(embed = log('SUCCESS', f'Successfully searched a link in {current_time_ms() - start_time}ms', f'URL: {url}', search_result['anchor']))



@tree.command(name = 'searchtrack', description = 'Search for a track') 
async def self(interaction: discord.Interaction, artist: str, track: str):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		search_result = await search_track(artist, track)
	except Exception as error:
		await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
		await logs_channel.send(embed = log('ERROR', f'When executing /searchtrack - "{error}"', f'Artist: "{artist}"\nTrack: "{track}"'))
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find your track. Please check for typos in your command and try again!"))
		await logs_channel.send(embed = log('FAILURE', f'Unsuccessfully executed command /searchtrack', f'Artist: "{artist}"\nTrack: "{track}"'))

	else:
		embed = await interaction.followup.send(embed = success_embed(search_result['track'], search_result['artists'], search_result['cover'], search_result['anchor']))
		await add_reactions(embed, ['👍','👎'])
		await logs_channel.send(embed = log('SUCCESS', f'Successfully executed command /searchtrack in {current_time_ms() - start_time}ms', f'Artist: "{artist}"\nTrack: "{track}"', search_result['anchor']))



@tree.command(name = 'searchalbum', description = 'Search for an album')
async def self(interaction: discord.Interaction, artist: str, album: str):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		search_result = await search_album(artist, album)
	except Exception as error:
		await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"),)
		await logs_channel.send(embed = log('ERROR', f'When running command /searchalbum - "{error}"', f'Artist: "{artist}"\nAlbum: "{album}"'))
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find your album. Please check for typos in your command and try again!"))
		await logs_channel.send(embed = log('FAILURE', f'Unsuccessfully executed command /searchalbum', f'Artist: "{artist}"\nAlbum: "{album}"'))

	else:
		embed = await interaction.followup.send(embed = success_embed(search_result['album'], search_result['artists'], search_result['cover'], search_result['anchor']))
		await add_reactions(embed, ['👍','👎'])
		await logs_channel.send(embed = log('SUCCESS', f'Successfully executed command /searchalbum in {current_time_ms() - start_time}ms', f'Artist: "{artist}"\nAlbum: "{album}"', search_result['anchor']))



@tree.command(name = 'lookup', description = 'Look up a track or album from its link')
async def self(interaction: discord.Interaction, link: str):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		music_data = await get_music_data(link)
		data = music_data['data']
		url_type = music_data['url_type']
	except:
		await interaction.followup.send(embed = fail_embed("The link provided isn't a valid music link."))
		await logs_channel.send(embed = log('FAILURE', 'Invalid URL', f'URL: {link}'))
		return None

	try:
		if url_type == 'track':
			data['track'] = remove_feat(data['track'])
			search_result = await search_track_from_url_data(max(data['artists'], key = len), data['track'])
			title = search_result['track']
		elif url_type == 'album':
			search_result = await search_album_from_url_data(max(data['artists'], key = len), data['album'])
			title = search_result['album']
	except Exception as error:
		await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"))
		await logs_channel.send(embed = log('ERROR', f'When executing /lookup - "{error}"', f'URL: "{link}"'))
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find anything regarding your link. Make sure you haven't accidentally typed anything in it and try again!"))
		await logs_channel.send(embed = log('FAILURE', f'Unsuccessfully executed command /lookup',f'URL: "{link}"'))

	else:
		embed = await interaction.followup.send(embed = success_embed(title, search_result['artists'], search_result['cover'], search_result['anchor']))
		await add_reactions(embed, ['👍','👎'])
		await logs_channel.send(embed = log('SUCCESS', f'Successfully executed command /lookup in {current_time_ms() - start_time}ms', f'URL: "{link}"', search_result['anchor']))



@tree.command(name = 'snoop', description = 'Get the song a user is listening to on Spotify')
async def self(interaction: discord.Interaction, user: discord.Member):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	guild = client.get_guild(interaction.guild.id)
	member = guild.get_member(user.id)
	replied = False

	for activity in member.activities:
		if isinstance(activity, Spotify):
			identifier = str(activity.track_id)
			data = await get_spotify_track(identifier)
			
			try:
				data['track'] = remove_feat(data['track'])
				search_result = await search_track_from_url_data(max(data['artists'], key = len), data['track'])
			except Exception as error:
				await interaction.followup.send(embed = fail_embed("An error occured while running your command."))
				await logs_channel.send(embed = log('ERROR', f'When running command /snoop - "{error}"', f'ID: {identifier}'))
				return None

			await interaction.followup.send(embed = success_embed(search_result['track'],search_result['artists'],search_result['cover'],search_result['anchor']))
			await logs_channel.send(embed = log('SUCCESS', f'Successfully ran the command /snoop in {current_time_ms() - start_time}ms', f'ID: {identifier}', search_result['anchor']))
			replied = True
		
	if replied == False:
		await interaction.followup.send(embed = fail_embed("That user doesn't appear to be listening to any Spotify track."))
		await logs_channel.send(embed = log('FAILURE', f'No Spotify playback detected when executing /snoop'))
		return None



@tree.context_menu(name = 'Search link(s)')
async def self(interaction: discord.Interaction, message: discord.Message):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	urls = find_urls(message.content)
	if urls != []:
		embeds = []
		parameters = []
		for url in urls:
			try:
				music_data = await get_music_data(url)
				data = music_data['data']
				url_type = music_data['url_type']
				if data == None:
					await logs_channel.send(embed = log('FAILURE', f'Failed to get track data from URL', f'URL: {url}'))
					continue
			except Exception as error:
				await logs_channel.send(embed = log('ERROR', f'When getting track data from URL - "{error}"', f'URL: {url}'))
				continue

			try:
				if url_type == 'track':
					data['track'] = remove_feat(data['track'])
					search_result = await search_track_from_url_data(max(data['artists'], key = len), data['track'])
					title = search_result['track']
				elif url_type == 'album':
					search_result = await search_album_from_url_data(max(data['artists'], key = len), data['album'])
					title = search_result['album']
			except Exception as error:
				await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"))
				await logs_channel.send(embed = log('ERROR', f'When executing "Search link(s)" - "{error}"', f'URL: "{url}"'))
				return None

			if search_result['anchor'] == '':
				embeds.append(fail_embed("I wasn't able to find anything regarding this link."))
				await logs_channel.send(embed = log('FAILURE', f'Unsuccessfully searched a URL with command "Search link(s)"',f'URL: "{url}"'))
				
			else:
				embeds.append(success_embed(title, search_result['artists'], search_result['cover'], search_result['anchor']))
				parameters.append(f'URL: {url}')
		if embeds != []:
			embed = await interaction.followup.send(embeds = embeds)
			await add_reactions(embed, ['👍','👎'])
			await logs_channel.send(embed = log('SUCCESS', f'Successfully executed command "Search link(s)" in {current_time_ms() - start_time}ms', '\n'.join(parameters)))
		else:
			await interaction.followup.send(embed = fail_embed("I wasn't able to find any music links in this message."))
			await logs_channel.send(embed = log('FAILURE', f'Found no music links when executing "Search link(s)"'))

	else:
		await interaction.followup.send(embed = fail_embed("I wasn't able to find any links in this message."))
		await logs_channel.send(embed = log('FAILURE', f'Found no links when executing "Search link(s)"'))



@tasks.loop(seconds = 60)
async def discord_presence():
	await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = presence_statuses[randint(0, len(presence_statuses)-1)]))



if is_internal:
	client.run(config['discord']['internal_token'])
else:
	client.run(config['discord']['token'])