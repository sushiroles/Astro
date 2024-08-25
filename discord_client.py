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



def success_embed(title: str, artists: list, cover: str, anchor: str, result_type: str):
	embed = discord.Embed(
		title = discord.utils.escape_markdown(f'{title}'),
		description = discord.utils.escape_markdown(f'by {', '.join(artists)}'),
		colour = get_average_color(cover),
	)
		
	embed.add_field(
		name = f'You can find this {result_type} on:',
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

			if is_music(url):
				try:
					data = await get_music_data(url)
					if data == None:
						await logs_channel.send(embed = log('FAILURE - Auto Link Lookup', f'Failed to get track data from URL', f'URL: {url}'))
						continue
					await message.add_reaction('❗')
				except Exception as error:
					await logs_channel.send(embed = log('ERROR - Auto Link Lookup', f'When getting track data from URL - "{error}"', f'URL: {url}'))
					continue
			else:
				continue

			while current_time_ms() - start_time <= 30000:
				if data['type'] == 'error':
					await logs_channel.send(embed = log('FAILURE - Auto Link Lookup', f'HTTP Error {data['response_status']}', f'URL: {url}'))
					return None
				try:
					if data['type'] == 'track':
						data['title'] = remove_feat(data['title'])
						search_result = await search_track(data['artists'][0], data['title'])
					elif data['type'] == 'album':
						search_result = await search_album(data['artists'][0], data['title'])
					break
				except Exception as error:
					await logs_channel.send(embed = log('NOTICE - Auto Link Lookup', f'Error when searching link - "{error}", retrying...', f'URL: {url}'))
					await asyncio.sleep(5)
			
			if current_time_ms() - start_time >= 30000:
				await message.add_reaction('⌛')
				await logs_channel.send(embed = log('FAILURE - Auto Link Lookup', f'Search timed out', f'URL: {url}'))
				if await check_reaction(message, '❗'):
					await message.remove_reaction('❗', client.user)
				continue

			if search_result['anchor'].count('\n') <= 1:
				await message.add_reaction('🤷')
				await logs_channel.send(embed = log('RETREAT - Auto Link Lookup', f'Insufficient results', f'URL: {url}'))
				if await check_reaction(message, '❗'):
					await message.remove_reaction('❗', client.user)
				continue
				
			if await check_reaction(message, '❗'):
				await message.remove_reaction('❗', client.user)

			embed = await message.reply(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type']), mention_author = False)
			await add_reactions(embed, ['👍','👎'])
			await logs_channel.send(embed = log('SUCCESS - Auto Link Lookup', f'Successfully searched a link in {current_time_ms() - start_time}ms', f'URL: {url}', search_result['log_anchor']))



@tree.command(name = 'searchtrack', description = 'Search for a track') 
async def self(interaction: discord.Interaction, artist: str, track: str):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		search_result = await search_track(artist, track)
	except Exception as error:
		await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
		await logs_channel.send(embed = log('ERROR - Track Search', f'{error}', f'Artist: "{artist}"\nTrack: "{track}"'))
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find your track. Please check for typos in your command and try again!"))
		await logs_channel.send(embed = log('FAILURE - Track Search', f'Unsuccessfully executed command', f'Artist: "{artist}"\nTrack: "{track}"'))

	else:
		embed = await interaction.followup.send(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type']))
		await add_reactions(embed, ['👍','👎'])
		await logs_channel.send(embed = log('SUCCESS - Track Search', f'Successfully executed command in {current_time_ms() - start_time}ms', f'Artist: "{artist}"\nTrack: "{track}"', search_result['log_anchor']))



@tree.command(name = 'searchalbum', description = 'Search for an album')
async def self(interaction: discord.Interaction, artist: str, album: str):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		search_result = await search_album(artist, album)
	except Exception as error:
		await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"),)
		await logs_channel.send(embed = log('ERROR - Album Search', f'{error}', f'Artist: "{artist}"\nAlbum: "{album}"'))
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find your album. Please check for typos in your command and try again!"))
		await logs_channel.send(embed = log('FAILURE - Album Search', f'Unsuccessfully executed command', f'Artist: "{artist}"\nAlbum: "{album}"'))

	else:
		embed = await interaction.followup.send(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type']))
		await add_reactions(embed, ['👍','👎'])
		await logs_channel.send(embed = log('SUCCESS - Album Search', f'Successfully executed command in {current_time_ms() - start_time}ms', f'Artist: "{artist}"\nAlbum: "{album}"', search_result['log_anchor']))



@tree.command(name = 'lookup', description = 'Look up a track or album from its link')
async def self(interaction: discord.Interaction, link: str):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		data = await get_music_data(link)
	except:
		await interaction.followup.send(embed = fail_embed("The link provided isn't a valid music link."))
		await logs_channel.send(embed = log('FAILURE - Link Lookup', 'Invalid URL', f'URL: {link}'))
		return None

	try:
		if data['type'] == 'error':
			await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"))
			await logs_channel.send(embed = log('FAILURE - Link Lookup', f'HTTP Error {data['response_status']}', f'URL: {link}'))
			return None
		if data['type'] == 'track':
			data['title'] = remove_feat(data['title'])
			search_result = await search_track(data['artists'][0], data['title'])
		elif data['type'] == 'album':
			search_result = await search_album(data['artists'][0], data['album'])
	except Exception as error:
		await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"))
		await logs_channel.send(embed = log('ERROR - Link Lookup', f'{error}', f'URL: "{link}"'))
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find anything regarding your link. Make sure you haven't accidentally typed anything in it and try again!"))
		await logs_channel.send(embed = log('FAILURE - Link Lookup', f'Unsuccessfully executed command',f'URL: "{link}"'))

	else:
		embed = await interaction.followup.send(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type']))
		await add_reactions(embed, ['👍','👎'])
		await logs_channel.send(embed = log('SUCCESS - Link Lookup', f'Successfully executed command in {current_time_ms() - start_time}ms', f'URL: "{link}"', search_result['log_anchor']))



@tree.command(name = 'snoop', description = 'Get the track a user is listening to on Spotify')
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
				if data['type'] == 'error':
					await interaction.followup.send(embed = fail_embed("An error occured while running your command. Please try again!"))
					await logs_channel.send(embed = log('ERROR - Snoop', f'{error}', f'ID: {identifier}'))
					return None
				data['title'] = remove_feat(data['title'])
				search_result = await search_track(data['artists'][0], data['title'])
			except Exception as error:
				await interaction.followup.send(embed = fail_embed("An error occured while running your command. Please try again!"))
				await logs_channel.send(embed = log('ERROR - Snoop', f'{error}', f'ID: {identifier}'))
				return None

			embed = await interaction.followup.send(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type']))
			await add_reactions(embed, ['👍','👎'])
			await logs_channel.send(embed = log('SUCCESS - Snoop', f'Successfully executed command in {current_time_ms() - start_time}ms', f'ID: {identifier}', search_result['log_anchor']))
			replied = True
		
	if replied == False:
		await interaction.followup.send(embed = fail_embed("That user doesn't appear to be listening to any Spotify track."))
		await logs_channel.send(embed = log('FAILURE - Snoop', f'No Spotify playback detected'))
		return None



@tree.command(name = 'coverart', description = 'Get the cover art of a track or album')
async def self(interaction: discord.Interaction, link: str):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		data = await get_music_data(link)
	except:
		await interaction.followup.send(embed = fail_embed("The link provided isn't a valid music link."))
		await logs_channel.send(embed = log('FAILURE - Get Cover Art', 'Invalid URL', f'URL: {link}'))
		return None

	try:
		if data['type'] == 'error':
			await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"))
			await logs_channel.send(embed = log('FAILURE - Get Cover Art', f'HTTP Error {data['response_status']}', f'URL: {link}'))
			return None
		if data['type'] == 'track':
			data['title'] = remove_feat(data['title'])
			search_result = await search_track(data['artists'][0], data['title'])
		elif data['type'] == 'album':
			search_result = await search_album(data['artists'][0], data['title'])
	except Exception as error:
		await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"))
		await logs_channel.send(embed = log('ERROR - Get Cover Art', f'{error}', f'URL: "{link}"'))
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find anything regarding your link. Make sure you haven't accidentally typed anything in it and try again!"))
		await logs_channel.send(embed = log('FAILURE - Get Cover Art', f'Unsuccessfully executed command',f'URL: "{link}"'))

	embed = discord.Embed(
		title = discord.utils.escape_markdown(f'{search_result['title']}'),
		description = discord.utils.escape_markdown(f'by {', '.join(search_result['artists'])}'),
		colour = get_average_color(search_result['cover']),
	)
	
	embed.set_image(url = search_result['cover'])
	embed.set_footer(text = 'Thank you for using Astro!')

	await interaction.followup.send(embed = embed)
	await logs_channel.send(embed = log('SUCCESS - Get Cover Art', f'Successfully executed command in {current_time_ms() - start_time}ms', f'URL: "{link}"', search_result['cover']))



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
				data = await get_music_data(url)
				if data == None:
					await logs_channel.send(embed = log('FAILURE - Context Menu Link Lookup', f'Failed to get track data from URL', f'URL: {url}'))
					continue
			except Exception as error:
				await logs_channel.send(embed = log('ERROR - Context Menu Link Lookup', f'{error}', f'URL: {url}'))
				continue

			try:
				if data['type'] == 'error':
					await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"))
					await logs_channel.send(embed = log('FAILURE - Context Menu Link Lookup', f'HTTP Error {data['response_status']}', f'URL: {url}'))
					return None
				if data['type'] == 'track':
					data['title'] = remove_feat(data['title'])
					search_result = await search_track(data['artists'][0], data['title'])
				elif data['type'] == 'album':
					search_result = await search_album(data['artists'][0], data['title'])
			except Exception as error:
				await interaction.followup.send(embed = fail_embed("An error has occured while running your command. Please try again!"))
				await logs_channel.send(embed = log('ERROR - Context Menu Link Lookup', f'{error}', f'URL: "{url}"'))
				return None

			if search_result['anchor'] == '':
				embeds.append(fail_embed("I wasn't able to find anything regarding this link."))
				await logs_channel.send(embed = log('FAILURE - Context Menu Link Lookup', f'Unsuccessfully searched a URL"',f'URL: "{url}"'))
				
			else:
				embeds.append(success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], data['type']))
				parameters.append(f'URL: {url}')
		if embeds != []:
			embed = await interaction.followup.send(embeds = embeds)
			await add_reactions(embed, ['👍','👎'])
			await logs_channel.send(embed = log('SUCCESS - Context Menu Link Lookup', f'Successfully executed command in {current_time_ms() - start_time}ms', '\n'.join(parameters)))
		else:
			await interaction.followup.send(embed = fail_embed("I wasn't able to find any music links in this message."))
			await logs_channel.send(embed = log('FAILURE - Context Menu Link Lookup', f'No music service URL-s found in message'))

	else:
		await interaction.followup.send(embed = fail_embed("I wasn't able to find any links in this message."))
		await logs_channel.send(embed = log('FAILURE - Context Menu Link Lookup', f'No URL-s at all found in message'))



@tasks.loop(seconds = 60)
async def discord_presence():
	await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = presence_statuses[randint(0, len(presence_statuses)-1)]))



if is_internal:
	client.run(config['discord']['internal_token'])
else:
	client.run(config['discord']['token'])