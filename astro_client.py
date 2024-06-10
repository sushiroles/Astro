import discord as discord 
import configparser
from discord import app_commands
from discord.ext import tasks
import json

from astroapi.nebula import *

config = configparser.ConfigParser()
config.read('tokens.ini')

discord_token = config['discord']['token']



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


'''
@client.event
async def on_message(message):
    print(message.content) 
'''


@tree.command(name = 'searchtrack', description = 'Search for a track') 
async def self(interaction: discord.Interaction, artist: str, track: str):
    search_result = search_track(artist,track)

    if search_result['artist_name'] == '' and search_result['track_name'] == '':
        embed = discord.Embed(
                            title=f'Oh no!',
                            colour=0xf5c000,
                        )
    
        embed.set_author(name=f'{await client.fetch_user(interaction.user.id)}')
    
        embed.add_field(
                        name='',
                        value="We weren't able to find your track. Please check for typos in your command and try again!",
                        inline=False
                    )
    
        embed.set_footer(text='Thank you for using MusicLinks!')

        with open('failed_commands.json', 'a', encoding='utf-8') as outfile: 
            json.dump({'request_type': 'track', 'requested_artist': search_result['requested_artist'], 'requested_track': search_result['requested_track']}, outfile, indent=4)

        await interaction.response.send_message(embed=embed, ephemeral = True)

    else:
        embed = discord.Embed(
                            title=f'{search_result['track_name']}',
                            description=f'by {search_result['artist_name']}',
                            colour=0xf5c000,
                        )
    
        embed.set_author(name=f'{await client.fetch_user(interaction.user.id)}')
    
        embed.add_field(name='You can find this track on:',
                value=search_result['service_anchor'],
                inline=False)
    
        embed.set_thumbnail(url=search_result['cover_art'])
        embed.set_footer(text='Thank you for using MusicLinks!')
        await interaction.response.send_message(embed=embed)


@tree.command(name = 'searchalbum', description = 'Search for an album') 
async def self(interaction: discord.Interaction, artist: str, album: str):
    search_result = search_album(artist,album)

    if search_result['artist_name'] == '' and search_result['album_name'] == '':
        embed = discord.Embed(
                            title=f'Oh no!',
                            colour=0xf5c000,
                        )
    
        embed.set_author(name=f'{await client.fetch_user(interaction.user.id)}')
    
        embed.add_field(
                        name='',
                        value="We weren't able to find your album. Please check for typos in your command and try again!",
                        inline=False
                    )
    
        embed.set_footer(text='Thank you for using MusicLinks!')

        with open('failed_commands.json', 'a', encoding='utf-8') as outfile:
            json.dump({'request_type': 'album', 'requested_artist': search_result['requested_artist'], 'requested_album': search_result['requested_album']}, outfile, indent=4)

        await interaction.response.send_message(embed=embed, ephemeral = True)

    else:
        embed = discord.Embed(
                            title=f'{search_result['album_name']}',
                            description=f'by {search_result['artist_name']}',
                            colour=0xf5c000,
                        )
    
        embed.set_author(name=f'{await client.fetch_user(interaction.user.id)}')
    
        embed.add_field(name='You can find this album on:',
                value=search_result['service_anchor'],
                inline=False)
    
        embed.set_thumbnail(url=search_result['cover_art'])
        embed.set_footer(text='Thank you for using MusicLinks!')
        await interaction.response.send_message(embed=embed)



client.run(discord_token)