import discord as discord 
import configparser
from discord import app_commands
from discord.ext import tasks

from nebula import *

is_internal = True

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
		log('STARTUP', 'Astro has successfully started up and connected to the Discord API')



client = Client() 
tree = app_commands.CommandTree(client)

@client.event
async def on_message(message):
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
			#elif is_youtube_music_track(url):
			#elif is_youtube_music_album(url):
			#elif is_deezer_track(url):
			#elif is_deezer_album(url):
			#elif is_tidal_track(url):
			#elif is_tidal_album(url):
			#elif is_bandcamp_track(url):
			#elif is_bandcamp_album(url):
			try:
				if url_type == 'track':
					search_result = search_track(bare_bones(data['artists'][0]), bare_bones(data['track']))[0]
				elif url_type == 'album':
					search_result = search_album(bare_bones(data['artists'][0]), bare_bones(data['album']))[0]
			except Exception as e:
				print(e)
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
			log('SUCCESS', f'Successfully passively searched a link in {current_time_ms() - start_time}ms --- url: "{url}"')



@tree.command(name = 'searchtrack', description = 'Search for a track') 
async def self(interaction: discord.Interaction, artist: str, track: str):
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
		log('CATASTROPHE', f'A catastrophic error occured running command /searchtrack --- error: "{error}" / artist: "{artist}" / track: "{track}"')
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
		log('FAILURE', f'Unsuccessfully executed command /searchtrack --- artist: "{artist}" / track: "{track}"')


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
		log('SUCCESS', f'Successfully executed command /searchtrack in {current_time_ms() - start_time}ms --- artist: "{artist}" / track: "{track}"')


@tree.command(name = 'searchalbum', description = 'Search for an album')
async def self(interaction: discord.Interaction, artist: str, album: str):
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
		log('CATASTROPHE', f'A catastrophic error occured running command /searchalbum --- error: "{error}" / artist: "{artist}" / album: "{album}"')
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
		log('FAILURE', f'Unsuccessfully executed command /searchalbum --- artist: "{artist}" / album: "{album}"')


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
		log('SUCCESS', f'Successfully executed command /searchalbum in {current_time_ms() - start_time}ms --- artist: "{artist}" / album: "{album}"')


if is_internal:
	client.run(config['discord']['internal_token'])
else:
	client.run(config['discord']['token'])