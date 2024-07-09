import discord as discord 
import configparser
from discord import app_commands
from discord.ext import tasks

from nebula import *

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
'''
@client.event
async def on_message(message):
	if message.content.find('https://open.spotify.com/track/') >= 0:
		start_time = current_time_ms()
		spotify_id = message.content[message.content.index('https://open.spotify.com/track/') : message.content.index('?')].replace('https://open.spotify.com/track/','')
		spotify_data = get_spotify_track(spotify_id)
		print(spotify_data)
		search_result = search_track(spotify_data['artist_name'].replace("'",''), spotify_data['track_name'].replace("'",''))

		embed = discord.Embed(
			title = f'{search_result['track_name']}',
			description = f'by {search_result['artist_name']}',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = 'You can find this track on:',
			value = search_result['service_anchor'],
			inline = False
		)
	
		embed.set_thumbnail(url = search_result['cover_art'])
		embed.set_footer(text = 'Thank you for using Astro!')
		await message.reply(embed = embed)
		log('SUCCESS', f'Successfully passively searched a Spotify track in {current_time_ms() - start_time}ms --- spotify_id: "{spotify_id}"')
	
	if message.content.find('https://open.spotify.com/album/') >= 0:
		start_time = current_time_ms()
		spotify_id = message.content[message.content.index('https://open.spotify.com/album/') : message.content.index('?')].replace('https://open.spotify.com/album/','')
		spotify_data = get_spotify_album(spotify_id)
		print(spotify_data)
		search_result = search_album(spotify_data['artist_name'].replace("'",''), spotify_data['album_name'].replace("'",''))

		embed = discord.Embed(
			title = f'{search_result['album_name']}',
			description = f'by {search_result['artist_name']}',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = 'You can find this album on:',
			value = search_result['service_anchor'],
			inline = False
		)
	
		embed.set_thumbnail(url = search_result['cover_art'])
		embed.set_footer(text = 'Thank you for using Astro!')
		await message.reply(embed = embed)
		log('SUCCESS', f'Successfully passively searched a Spotify album in {current_time_ms() - start_time}ms --- spotify_id: "{spotify_id}"')
	
	if message.content.find('https://open.spotify.com/track/') >= 0:
		start_time = current_time_ms()
		spotify_id = message.content[message.content.index('https://open.spotify.com/track/') : message.content.index('?')].replace('https://open.spotify.com/track/','')
		spotify_data = get_spotify_track(spotify_id)
		print(spotify_data)
		search_result = search_track(spotify_data['artist_name'].replace("'",''), spotify_data['track_name'].replace("'",''))

		embed = discord.Embed(
			title = f'{search_result['track_name']}',
			description = f'by {search_result['artist_name']}',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = 'You can find this track on:',
			value = search_result['service_anchor'],
			inline = False
		)
	
		embed.set_thumbnail(url = search_result['cover_art'])
		embed.set_footer(text = 'Thank you for using Astro!')
		await message.reply(embed = embed)
		log('SUCCESS', f'Successfully passively searched a Spotify track in {current_time_ms() - start_time}ms --- spotify_id: "{spotify_id}"')
	
	if message.content.find('https://open.spotify.com/album/') >= 0:
		start_time = current_time_ms()
		spotify_id = message.content[message.content.index('https://open.spotify.com/album/') : message.content.index('?')].replace('https://open.spotify.com/album/','')
		spotify_data = get_spotify_album(spotify_id)
		print(spotify_data)
		search_result = search_album(spotify_data['artist_name'].replace("'",''), spotify_data['album_name'].replace("'",''))

		embed = discord.Embed(
			title = f'{search_result['album_name']}',
			description = f'by {search_result['artist_name']}',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = 'You can find this album on:',
			value = search_result['service_anchor'],
			inline = False
		)
	
		embed.set_thumbnail(url = search_result['cover_art'])
		embed.set_footer(text = 'Thank you for using Astro!')
		await message.reply(embed = embed)
		log('SUCCESS', f'Successfully passively searched a Spotify album in {current_time_ms() - start_time}ms --- spotify_id: "{spotify_id}"')
'''

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
		

	if search_result['service_anchor'] == '':
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
			title = f'{search_result['track_name']}',
			description = f'by {', '.join(search_result['artist_name'])}',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = 'You can find this track on:',
			value = search_result['service_anchor'],
			inline = False
		)
	
		embed.set_thumbnail(url = search_result['cover_art'])
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
		

	if search_result['service_anchor'] == '':
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
			title = f'{search_result['album_name']}',
			description = f'by {', '.join(search_result['artist_name'])}',
			colour = 0xf5c000,
		)
		
		embed.add_field(
			name = 'You can find this album on:',
			value = search_result['service_anchor'],
			inline = False
		)
	
		embed.set_thumbnail(url = search_result['cover_art'])
		embed.set_footer(text = 'Thank you for using Astro!')
		await interaction.followup.send(embed = embed)
		log('SUCCESS', f'Successfully executed command /searchalbum in {current_time_ms() - start_time}ms --- artist: "{artist}" / album: "{album}"')



client.run(config['discord']['token'])