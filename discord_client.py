import discord as discord 
from discord import app_commands
from discord.ext import tasks

import configparser
from random import randint
from time import sleep

from app_services import *



config = configparser.ConfigParser()
config.read('tokens.ini')



class Client(discord.Client): 
	def __init__(self):
		discordintents = discord.Intents.default() 		
		discordintents.message_content = True			
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



@client.event
async def on_message(message):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	urls = find_urls(message.content)
	if urls != []:
		for url in urls:
			music_data = get_music_data(url)
			start_time = music_data['start_time']
			data = music_data['data']
			url_type = music_data['url_type']

			if url_type != '':
				try:
					if url_type == 'track':
						search_result = search_track(data['artists'][0], data['track'])[0]
					elif url_type == 'album':
						search_result = search_album(data['artists'][0], data['album'])[0]
				except Exception as error:
					await logs_channel.send(embed = log('NOTICE', f'Error when searching link - "{error}", retrying in 5 seconds', f'URL: {url}'))
					sleep(5)
					try:
						if url_type == 'track':
							search_result = search_track(data['artists'][0], data['track'])[0]
						elif url_type == 'album':
							search_result = search_album(data['artists'][0], data['album'])[0]
					except Exception as error:
						await message.add_reaction('\U0001F613')
						await logs_channel.send(embed = log('ERROR', f'When searching link - "{error}"', f'URL: {url}'))
						return None

				if search_result['anchor'].count('\n') <= 1:
					await message.add_reaction('\U0001F937')
					await logs_channel.send(embed = log('RETREAT', f'Insufficient results', f'URL: {url}'))
					return None

				if url_type == 'track':
					embed = discord.Embed(
						title = f'{search_result['track']}',
						description = f'by {', '.join(search_result['artists'])}',
						colour = 0xf5c000,
					)
				elif url_type == 'album':
					embed = discord.Embed(
						title = f'{search_result['album']}',
						description = f'by {', '.join(search_result['artists'])}',
						colour = 0xf5c000,
					)
				if url_type == 'track':
					embed.add_field(
						name = 'You can find this track on:',
						value = search_result['anchor'],
						inline = False
					)
				elif url_type == 'album':
					embed.add_field(
						name = 'You can find this album on:',
						value = search_result['anchor'],
						inline = False
					)
				
				embed.set_thumbnail(url = search_result['cover'])
				embed.set_footer(text = 'Thank you for using Astro!')
				await message.reply(embed = embed)
				await logs_channel.send(embed = log('SUCCESS', f'Successfully searched a link in {current_time_ms() - start_time}ms', f'URL: {url}'))



@tree.command(name = 'searchtrack', description = 'Search for a track') 
async def self(interaction: discord.Interaction, artist: str, track: str):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		search_result = search_track(bare_bones(artist), bare_bones(track))[0]
	except Exception as error:
		embed = discord.Embed(
			title = f'Oh no!',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = '',
			value = "An error has occured while running your command. Please try again!",
			inline = False
		)
	
		embed.set_footer(text = 'Thank you for using Astro!')
		await interaction.followup.send(embed = embed, ephemeral = True)
		await logs_channel.send(embed = log('ERROR', f'When executing /searchtrack - "{error}"', f'Artist: "{artist}"\nTrack: "{track}"'))
		return None
		


	if search_result['anchor'] == '':
		embed = discord.Embed(
			title = f'Oh no!',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = '',
			value = "We weren't able to find your track. Please check for typos in your command and try again!",
			inline = False
		)
	
		embed.set_footer(text = 'Thank you for using Astro!')
		await interaction.followup.send(embed = embed, ephemeral = True)
		await logs_channel.send(embed = log('FAILURE', f'Unsuccessfully executed command /searchtrack',f'Artist: "{artist}"\nTrack: "{track}"'))


	else:
		embed = discord.Embed(
			title = f'{search_result['track']}',
			description = f'by {', '.join(search_result['artists'])}',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = 'You can find this track on:',
			value = search_result['anchor'],
			inline = False
		)
	
		embed.set_thumbnail(url = search_result['cover'])
		embed.set_footer(text = 'Thank you for using Astro!')
		await interaction.followup.send(embed = embed)
		await logs_channel.send(embed = log('SUCCESS', f'Successfully executed command /searchtrack in {current_time_ms() - start_time}ms', f'Artist: "{artist}"\nTrack: "{track}"'))



@tree.command(name = 'searchalbum', description = 'Search for an album')
async def self(interaction: discord.Interaction, artist: str, album: str):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	start_time = current_time_ms()
	await interaction.response.defer()
	try:
		search_result = search_album(bare_bones(artist), bare_bones(album))[0]
	except Exception as error:
		embed = discord.Embed(
			title = f'Oh no!',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = '',
			value = "An error has occured while running your command. Please try again!",
			inline = False
		)
	
		embed.set_footer(text = 'Thank you for using Astro!')
		await interaction.followup.send(embed = embed, ephemeral = True)
		await logs_channel.send(embed = log('ERROR', f'When running command /searchalbum - "{error}"', f'Artist: "{artist}"\nAlbum: "{album}"'))
		return None


	if search_result['anchor'] == '':
		embed = discord.Embed(
			title = f'Oh no!',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = '',
			value = "We weren't able to find your album. Please check for typos in your command and try again!",
			inline = False
		)
	
		embed.set_footer(text = 'Thank you for using Astro!')

		await interaction.followup.send(embed = embed, ephemeral = True)
		await logs_channel.send(embed = log('FAILURE', f'Unsuccessfully executed command /searchalbum', f'Artist: "{artist}"\nAlbum: "{album}"'))


	else:
		embed = discord.Embed(
			title = f'{search_result['album']}',
			description = f'by {', '.join(search_result['artists'])}',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = 'You can find this album on:',
			value = search_result['anchor'],
			inline = False
		)
	
		embed.set_thumbnail(url = search_result['cover'])
		embed.set_footer(text = 'Thank you for using Astro!')
		await interaction.followup.send(embed = embed)
		await logs_channel.send(embed = log('SUCCESS', f'Successfully executed command /searchalbum in {current_time_ms() - start_time}ms', f'Artist: "{artist}"\nAlbum: "{album}"'))



@tasks.loop(seconds = 60)
async def discord_presence():
	await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = presence_statuses[randint(0, len(presence_statuses)-1)]))



if is_internal:
	client.run(config['discord']['internal_token'])
else:
	client.run(config['discord']['token'])