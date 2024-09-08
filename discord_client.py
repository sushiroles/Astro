import discord as discord 
from discord import app_commands
from discord import Spotify
from discord.ext import tasks

import configparser
from random import randint

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



version = '1.2'
client = Client()
tree = app_commands.CommandTree(client)
is_internal = True
presence_statuses = open('discord_presence.txt','r').readlines()



def success_embed(title: str, artists: list, cover: str, anchor: str, result_type: str, is_explicit: bool = None, particular_user: discord.Member = None):
	embed = discord.Embed(
		title = discord.utils.escape_markdown(f'{title}{track_is_explicit(is_explicit)}'),
		description = discord.utils.escape_markdown(f'by {', '.join(artists)}'),
		colour = get_average_color(cover),
	)

	if particular_user != None:
		embed.set_author(
			name = f'@{particular_user.name} is listening to',
			icon_url = particular_user.avatar
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
async def on_ready():
	await client.wait_until_ready()
	if not client.synced:
		await tree.sync()
		client.synced = True
	if not discord_presence.is_running():
		discord_presence.start()

	logs_channel = log_channel
	embed = discord.Embed(
		title = f'READY',
		colour = 0x66f500,
	)
	embed.add_field(
		name = 'Current version',
		value = f'> `{version}`',
		inline = True
	)
	embed.add_field(
		name = 'Is internal?',
		value = f'> `{is_internal}`',
		inline = True
	)
	embed.add_field(
		name = 'Start time',
		value = f'<t:{current_time()}:F>',
		inline = True
	)
	embed.add_field(
		name = 'Stats',
		value = f'>>> In `{len(client.guilds)}` servers\n Accessible to `{len(client.users)}` users',
		inline = True
	)
	
	await log('meow', 'mrrp', 'mreow', ':3', embed, logs_channel)



@client.event
async def on_message(message):
	logs_channel = log_channel
	urls = find_urls(message.content)
	if urls != []:
		for url in urls:
			start_time = current_time_ms()

			if is_music(url):
				try:
					data = await get_music_data(url)
					if data['type'] == 'empty_response':
						await log('FAILURE - Auto Link Lookup', f'Empty response', f'URL: `{url}`', logs_channel = logs_channel)
						continue
					if data['type'] == 'error':
						await log('FAILURE - Auto Link Lookup', f'HTTP Error {data['response_status']}', f'URL: `{url}`', logs_channel = logs_channel)
						continue
					await message.add_reaction('❗')
				except Exception as error:
					await log('ERROR - Auto Link Lookup', f'{error}', f'URL: `{url}`', logs_channel = logs_channel)
					continue
			else:
				continue

			while current_time_ms() - start_time <= 30000:
				try:
					if data['type'] == 'track':
						data['title'] = remove_feat(data['title'])
						search_result = await search_track(data['artists'][0], data['title'], data['collection_name'], data['is_explicit'])
					elif data['type'] == 'album':
						search_result = await search_album(data['artists'][0], data['title'], data['year'])
					break
				except Exception as error:
					await log('NOTICE - Auto Link Lookup', f'Error when searching link - "{error}", retrying...', f'URL: `{url}`', logs_channel = logs_channel)
					await asyncio.sleep(5)

			if current_time_ms() - start_time >= 30000:
				await message.add_reaction('⌛')
				await log('FAILURE - Auto Link Lookup', f'Search timed out', f'URL: `{url}`', logs_channel = logs_channel)
				if await check_reaction(message, '❗'):
					await message.remove_reaction('❗', client.user)
				continue

			if search_result['anchor'].count('\n') <= 1:
				await message.add_reaction('🤷')
				await log('RETREAT - Auto Link Lookup', f'Insufficient results', f'URL: `{url}`', logs_channel = logs_channel)
				if await check_reaction(message, '❗'):
					await message.remove_reaction('❗', client.user)
				continue

			if search_result['anchor'].count('\n') == 2:
				if search_result['type'] == 'track':
					search_result['title'] = remove_feat(search_result['title'])
					search_result = await search_track(search_result['artists'][0], search_result['title'], search_result['collection_name'], search_result['is_explicit'])
				elif search_result['type'] == 'album':
					search_result = await search_album(search_result['artists'][0], search_result['title'], search_result['year'])
				
			if await check_reaction(message, '❗'):
				await message.remove_reaction('❗', client.user)

			embed = await message.reply(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type'], (search_result['is_explicit'] if search_result['type'] == 'track' else None)), mention_author = False)
			await add_reactions(embed, ['👍','👎'])
			await log('SUCCESS - Auto Link Lookup', f'Successfully searched a link in {current_time_ms() - start_time}ms', f'URL: `{url}`', search_result['log_anchor'], logs_channel = logs_channel)



@tree.command(name = 'searchtrack', description = 'Search for a track')
@app_commands.describe(artist = 'The name of the artist of the track you want to look up (ex. "Radiohead")')
@app_commands.describe(track = 'The title of the track you want to look up (ex. "Bodysnatchers")')
@app_commands.describe(from_album = 'The album or collection of the track you want to look up, helps with precision (ex. "In Rainbows")')
@app_commands.describe(is_explicit = 'Whether the track you want to look up has explicit content (has the little [E] badge next to its name on streaming platforms), helps with precision')
@app_commands.user_install()
async def searchtrack(interaction: discord.Interaction, artist: str, track: str, from_album: str = None, is_explicit: bool = None):
	logs_channel = log_channel
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		search_result = await search_track(artist, track, from_album, is_explicit)
	except Exception as error:
		await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
		await log('ERROR - Track Search', f'{error}', f'Artist: `{artist}`\nTrack: `{track}`\nCollection: `{from_album}`\nIs explicit? `{is_explicit}`', logs_channel = logs_channel)
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find your track. Please check for typos in your command and try again!"))
		await log('FAILURE - Track Search', f'Unsuccessfully executed command', f'Artist: `{artist}`\nTrack: `{track}`\nCollection: `{from_album}`\nIs explicit? `{is_explicit}`', logs_channel = logs_channel)
		return None

	if search_result['anchor'].count('\n') <= 2:
		try:
			search_result = await search_track(search_result['artists'][0], search_result['title'], search_result['collection_name'], search_result['is_explicit'])
		except Exception as error:
			await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
			await log('ERROR - Track Search', f'{error}', f'Artist: `{artist}`\nTrack: `{track}`\nCollection: `{from_album}`\nIs explicit? `{is_explicit}`', logs_channel = logs_channel)
			return None

	embed = await interaction.followup.send(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type'], search_result['is_explicit']))
	await add_reactions(embed, ['👍','👎'])
	end_time = current_time_ms()
	await log('SUCCESS - Track Search', f'Successfully executed command in {end_time - start_time}ms', f'Artist: `{artist}`\nTrack: `{track}`\nCollection: `{from_album}`\nIs explicit? `{is_explicit}`', search_result['log_anchor'], logs_channel = logs_channel)



@tree.command(name = 'searchalbum', description = 'Search for an album')
@app_commands.describe(artist = 'The artist of the album you want to look up (ex. "Kendrick Lamar")')
@app_commands.describe(album = 'The title of the album you want to look up (ex. "To Pimp A Butterfly")')
@app_commands.describe(year = 'The release year of the album you want to look up, helps with precision (ex. "2015")')
@app_commands.user_install()
async def searchalbum(interaction: discord.Interaction, artist: str, album: str, year: str = None):
	logs_channel = log_channel
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		search_result = await search_album(artist, album, year)
	except Exception as error:
		await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'),)
		await log('ERROR - Album Search', f'{error}', f'Artist: `{artist}`\nAlbum: `{album}`\nYear: `{year}`', logs_channel = logs_channel)
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find your album. Please check for typos in your command and try again!"))
		await log('FAILURE - Album Search', f'Unsuccessfully executed command', f'Artist: `{artist}`\nAlbum: `{album}`\nYear: `{year}`', logs_channel = logs_channel)
		return None

	if search_result['anchor'].count('\n') <= 2:
		try:
			search_result = await search_album(search_result['artists'][0], search_result['title'], search_result['year'])
		except Exception as error:
			await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
			await log('FAILURE - Album Search', f'Unsuccessfully executed command', f'Artist: `{artist}`\nAlbum: `{album}`\nYear: `{year}`', logs_channel = logs_channel)
			return None

	embed = await interaction.followup.send(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type']))
	await add_reactions(embed, ['👍','👎'])
	end_time = current_time_ms()
	await log('SUCCESS - Album Search', f'Successfully executed command in {end_time - start_time}ms', f'Artist: `{artist}`\nAlbum: `{album}`\nYear: `{year}`', search_result['log_anchor'], logs_channel = logs_channel)



@tree.command(name = 'lookup', description = 'Look up a track or album from its link')
@app_commands.describe(link = 'The link of the track or album you want to look up')
@app_commands.user_install()
async def lookup(interaction: discord.Interaction, link: str):
	logs_channel = log_channel
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		data = await get_music_data(link)
	except:
		await interaction.followup.send(embed = fail_embed("The link provided isn't a valid music link."))
		await log('FAILURE - Link Lookup', 'Invalid URL', f'URL: `{link}`', logs_channel = logs_channel)
		return None

	try:
		if data['type'] == 'error':
			await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
			await log('FAILURE - Link Lookup', f'HTTP Error {data['response_status']}', f'URL: `{link}`', logs_channel = logs_channel)
			return None
		if data['type'] == 'track':
			data['title'] = remove_feat(data['title'])
			search_result = await search_track(data['artists'][0], data['title'], data['collection_name'], data['is_explicit'])
		elif data['type'] == 'album':
			search_result = await search_album(data['artists'][0], data['title'], data['year'])
	except Exception as error:
		await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
		await log('ERROR - Link Lookup', f'{error}', f'URL: `{link}`', logs_channel = logs_channel)
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find anything regarding your link. Make sure you haven't accidentally typed anything in it and try again!"))
		await log('FAILURE - Link Lookup', f'Unsuccessfully executed command',f'URL: `{link}`', logs_channel = logs_channel)
		return None

	if search_result['anchor'].count('\n') <= 2:
		try:
			if search_result['type'] == 'track':
				search_result['title'] = remove_feat(search_result['title'])
				search_result = await search_track(search_result['artists'][0], search_result['title'], search_result['collection_name'], search_result['is_explicit'])
			elif search_result['type'] == 'album':
				search_result = await search_album(search_result['artists'][0], search_result['title'])
		except Exception as error:
			await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
			await log('ERROR - Link Lookup', f'{error}', f'URL: `{link}`', logs_channel = logs_channel)
			return None

	embed = await interaction.followup.send(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type'], (search_result['is_explicit'] if search_result['type'] == 'track' else None)))
	await add_reactions(embed, ['👍','👎'])
	end_time = current_time_ms()
	await log('SUCCESS - Link Lookup', f'Successfully executed command in {end_time - start_time}ms', f'URL: `{link}`', search_result['log_anchor'], logs_channel = logs_channel)



@tree.command(name = 'snoop', description = 'Get the track a user is listening to on Spotify')
@app_commands.describe(user = 'The user you want to snoop on')
@app_commands.describe(ephemeral = 'Whether the executed command should be ephemeral (only visible to you), false by default')
async def snoop(interaction: discord.Interaction, user: discord.Member, ephemeral: bool = False):
	logs_channel = log_channel
	start_time = current_time_ms()
	await interaction.response.defer(ephemeral = ephemeral)

	guild = client.get_guild(interaction.guild.id)
	member = guild.get_member(user.id)
	replied = False

	for activity in member.activities:
		if isinstance(activity, Spotify):
			identifier = str(activity.track_id)
			data = await get_spotify_track(identifier)
			
			try:
				if data['type'] == 'error':
					await interaction.followup.send(embed = fail_embed('An error occured while running your command. Please try again!'))
					await log('ERROR - Snoop', f'{error}', f'ID: `{identifier}`', logs_channel = logs_channel)
					return None
				data['title'] = remove_feat(data['title'])
				search_result = await search_track(data['artists'][0], data['title'], data['collection_name'], data['is_explicit'])
			except Exception as error:
				await interaction.followup.send(embed = fail_embed('An error occured while running your command. Please try again!'))
				await log('ERROR - Snoop', f'{error}', f'ID: `{identifier}`', logs_channel = logs_channel)
				return None

			if search_result['anchor'].count('\n') <= 2:
				try:
					search_result['title'] = remove_feat(search_result['title'])
					search_result = await search_track(search_result['artists'][0], search_result['title'], search_result['collection_name'], search_result['is_explicit'])
				except Exception as error:
					await interaction.followup.send(embed = fail_embed('An error occured while running your command. Please try again!'))
					await log('ERROR - Snoop', f'{error}', f'ID: `{identifier}`', logs_channel = logs_channel)
					return None

			embed = await interaction.followup.send(embed = success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], search_result['type'], search_result['is_explicit'], user))
			await add_reactions(embed, ['👍','👎'])
			end_time = current_time_ms()
			await log('SUCCESS - Snoop', f'Successfully executed command in {end_time - start_time}ms', f'ID: `{identifier}`', search_result['log_anchor'], logs_channel = logs_channel)
			replied = True
		
	if replied == False:
		await interaction.followup.send(embed = fail_embed("That user doesn't appear to be listening to any Spotify track."))
		await log('FAILURE - Snoop', f'No Spotify playback detected', logs_channel = logs_channel)
		return None



@tree.command(name = 'coverart', description = 'Get the cover art of a track or album')
@app_commands.describe(link = 'The link of the track or album you want to retrieve the cover art from')
@app_commands.user_install()
async def coverart(interaction: discord.Interaction, link: str):
	logs_channel = log_channel
	start_time = current_time_ms()
	await interaction.response.defer()

	try:
		data = await get_music_data(link)
	except:
		await interaction.followup.send(embed = fail_embed("The link provided isn't a valid music link."))
		await log('FAILURE - Cover Art Showcase', 'Invalid URL', f'URL: `{link}`', logs_channel = logs_channel)
		return None

	try:
		if data['type'] == 'error':
			await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
			await log('FAILURE - Cover Art Showcase', f'HTTP Error {data['response_status']}', f'URL: `{link}`', logs_channel = logs_channel)
			return None
		if data['type'] == 'track':
			data['title'] = remove_feat(data['title'])
			search_result = await search_track(data['artists'][0], data['title'], data['collection_name'], data['is_explicit'])
		elif data['type'] == 'album':
			search_result = await search_album(data['artists'][0], data['title'], data['year'])
	except Exception as error:
		await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
		await log('ERROR - Cover Art Showcase', f'{error}', f'URL: `{link}`', logs_channel = logs_channel)
		return None

	if search_result['anchor'] == '':
		await interaction.followup.send(embed = fail_embed("I wasn't able to find anything regarding your link. Make sure you haven't accidentally typed anything in it and try again!"))
		await log('FAILURE - Cover Art Showcase', f'Unsuccessfully executed command',f'URL: `{link}`', logs_channel = logs_channel)
		return None

	embed = discord.Embed(
		title = discord.utils.escape_markdown(f'{search_result['title']}{track_is_explicit(search_result['is_explicit'])}'),
		description = discord.utils.escape_markdown(f'by {', '.join(search_result['artists'])}'),
		colour = get_average_color(search_result['cover']),
	)
	
	embed.set_image(url = search_result['cover'])
	embed.set_footer(text = 'Thank you for using Astro!')

	await interaction.followup.send(embed = embed)
	end_time = current_time_ms()
	await log('SUCCESS - Get Cover Art', f'Successfully executed command in {end_time - start_time}ms', f'URL: `{link}`', search_result['cover'], logs_channel = logs_channel)



@tree.context_menu(name = 'Search music link(s)')
@app_commands.user_install()
async def contextmenulookup(interaction: discord.Interaction, message: discord.Message):
	logs_channel = log_channel
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
					await log('FAILURE - Context Menu Link Lookup', f'Failed to get track data from URL', f'URL: `{url}`', logs_channel = logs_channel)
					continue
			except Exception as error:
				await log('ERROR - Context Menu Link Lookup', f'{error}', f'URL: `{url}`', logs_channel = logs_channel)
				continue

			try:
				if data['type'] == 'error':
					await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
					await log('FAILURE - Context Menu Link Lookup', f'HTTP Error {data['response_status']}', f'URL: {url}', logs_channel = logs_channel)
					return None
				if data['type'] == 'track':
					data['title'] = remove_feat(data['title'])
					search_result = await search_track(data['artists'][0], data['title'], data['collection_name'], data['is_explicit'])
				elif data['type'] == 'album':
					search_result = await search_album(data['artists'][0], data['title'], data['year'])
			except Exception as error:
				await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
				await log('ERROR - Context Menu Link Lookup', f'{error}', f'URL: `{url}`', logs_channel = logs_channel)
				return None
			
			if search_result['anchor'] == '':
				embeds.append(fail_embed("I wasn't able to find anything regarding this link."))
				await log('FAILURE - Context Menu Link Lookup', f'Unsuccessfully searched a URL',f'URL: `{url}`', logs_channel = logs_channel)
				continue

			if search_result['anchor'].count('\n') <= 2:
				try:
					if search_result['type'] == 'track':
						search_result['title'] = remove_feat(search_result['title'])
						search_result = await search_track(search_result['artists'][0], search_result['title'], search_result['collection_name'], search_result['is_explicit'])
					elif search_result['type'] == 'album':
						search_result = await search_album(search_result['artists'][0], search_result['title'], search_result['year'])
				except Exception as error:
					await interaction.followup.send(embed = fail_embed('An error has occured while running your command. Please try again!'))
					await log('ERROR - Context Menu Link Lookup', f'{error}', f'URL: `{url}`', logs_channel = logs_channel)
					return None
			
			else:
				embeds.append(success_embed(search_result['title'], search_result['artists'], search_result['cover'], search_result['anchor'], data['type'], (search_result['is_explicit'] if search_result['type'] == 'track' else None)))
				parameters.append(f'URL: `{url}`')
		if embeds != []:
			embed = await interaction.followup.send(embeds = embeds)
			await add_reactions(embed, ['👍','👎'])
			end_time = current_time_ms()
			await log('SUCCESS - Context Menu Link Lookup', f'Successfully executed command in {end_time - start_time}ms', '\n'.join(parameters), logs_channel = logs_channel)
		else:
			await interaction.followup.send(embed = fail_embed("I wasn't able to find any music links in this message."))
			await log('FAILURE - Context Menu Link Lookup', f'No music service URL-s found in message', logs_channel = logs_channel)

	else:
		await interaction.followup.send(embed = fail_embed("I wasn't able to find any links in this message."))
		await log('FAILURE - Context Menu Link Lookup', f'No URL-s at all found in message', logs_channel = logs_channel)



@tasks.loop(seconds = 60)
async def discord_presence():
	await client.change_presence(activity = discord.Activity(
		type = discord.ActivityType.listening,
		name = presence_statuses[randint(0, len(presence_statuses)-1)],
	))



if is_internal:
	log_channel = str(config['discord']['internal_logs_channel'])
	client.run(config['discord']['internal_token'])
else:
	log_channel = str(config['discord']['logs_channel'])
	client.run(config['discord']['token'])