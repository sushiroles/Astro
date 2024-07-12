import discord as discord 
import configparser
from discord import app_commands

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



client = Client() 
tree = app_commands.CommandTree(client)
is_internal = True

@client.event
async def on_message(message):
	logs_channel = client.get_channel(int(config['discord']['logs_channel']))
	urls = find_urls(message.content)
	if urls != []:
		for url in urls:
			start_time = current_time_ms()
			url_type = ''
			data = {}
			if is_spotify_track(url):
				start_time = current_time_ms()
				identifier = get_spotify_id(url)
				data = get_spotify_track(identifier)
				url_type = 'track'
			elif is_spotify_album(url):
				start_time = current_time_ms()
				identifier = get_spotify_id(url)
				data = get_spotify_album(identifier)
				url_type = 'album'
			elif is_apple_music_track(url):
				start_time = current_time_ms()
				identifier = get_apple_music_track_id(url)
				data = get_apple_music_track(identifier)
				url_type = 'track'
			elif is_apple_music_album(url):
				start_time = current_time_ms()
				identifier = get_apple_music_album_id(url)
				data = get_apple_music_album(identifier)
				url_type = 'album'
			elif is_youtube_music_track(url):
				start_time = current_time_ms()
				identifier = get_youtube_music_track_id(url)
				data = get_youtube_music_track(identifier)
				url_type = 'track'
			elif is_youtube_music_album(url):
				start_time = current_time_ms()
				identifier = get_youtube_music_album_id(url)
				data = get_youtube_music_album(identifier)
				url_type = 'album'
			elif is_deezer_track(url):
				start_time = current_time_ms()
				identifier = get_deezer_track_id(url)
				data = get_deezer_track(identifier)
				url_type = 'track'
			elif is_deezer_album(url):
				start_time = current_time_ms()
				identifier = get_deezer_album_id(url)
				data = get_deezer_album(identifier)
				url_type = 'album'
			elif is_tidal_track(url):
				start_time = current_time_ms()
				identifier = get_tidal_track_id(url)
				data = get_tidal_track(identifier)
				url_type = 'track'
			elif is_tidal_album(url):
				start_time = current_time_ms()
				identifier = get_tidal_album_id(url)
				data = get_tidal_album(identifier)
				url_type = 'album'
			elif is_bandcamp_track(url):
				start_time = current_time_ms()
				data = get_bandcamp_track_parameters(url)
				url_type = 'track'
			elif is_bandcamp_album(url):
				start_time = current_time_ms()
				data = get_bandcamp_album_parameters(url)
				url_type = 'album'
			if url_type != '':
				try:
					if url_type == 'track':
						search_result = search_track(bare_bones(data['artists'][0]), bare_bones(data['track']))[0]
					elif url_type == 'album':
						search_result = search_album(bare_bones(data['artists'][0]), bare_bones(data['album']))[0]
				except Exception as error:
					await logs_channel.send(embed = log('ERROR', f'When searching link - "{error}"', f'URL: {url}'))
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
		search_result = search_track(artist, track)[0]
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
		

	if search_result['track'] == '':
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
		search_result = search_album(artist, album)[0]
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


	if search_result['album'] == '':
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


if is_internal:
	client.run(config['discord']['internal_token'])
else:
	client.run(config['discord']['token'])