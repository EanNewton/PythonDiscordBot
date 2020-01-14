#!/usr/bin/python3

import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#client = discord.Client()
bot = commands.Bot(command_prefix='!')
bot.load_extension('cog')

randQuotes = [
		'"I <3 butt plugs" - Roxy9321',
		'"Can I be Mod"- Lensing',
		(
			'I\'m very proud of my 1 chest hair.\n'	
			'What im trying to say here is that... your tits are beautiful'
		),
]

@bot.event
async def on_ready():
	'''
	#Naive guild find
	for guild in client.guilds:
		if guild.name == GUILD:
			break
	#Another way
	guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
	'''
	#Cleanest way
	#get() actually uses the attrs keyword args to build a predicate
	#which it then uses to call find()
	global guildHandle
	guildHandle = discord.utils.get(bot.guilds, name=GUILD)
	
			
	print(
	f'{bot.user} has connected to Discord!\n'
	f'{guildHandle.name}(id: {guildHandle.id})'
	)
	
	members = '\n - '.join([member.name for member in guildHandle.members])
	print(f'Guild Members:\n - {members}')
	
@bot.event 
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
			f'Hello {member.name}, welcome to {guildHandle.name}!'
	)
	
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CheckFailure):
		await ctx.send(f'{error}')
	
@bot.command(name='quote', help='Check out our fam quotes!')
async def randquote(ctx):
	response = random.choice(randQuotes)
	await ctx.send(response)

@bot.command(name='roll', help='!roll [AMOUNT] [SIDES] dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
	dice = [
		str(random.choice(range(1, number_of_sides + 1)))
		for _ in range(number_of_dice)
	]
	await ctx.send(', '.join(dice))
	
@bot.command(name='create-channel', help='Create a new channel.')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name):
	existing_channel = discord.utils.get(guildHandle.channels, name=channel_name)
	if not existing_channel:
		print(f'Creating new channel: {channel_name}')
		await guildHandle.create_text_channel(channel_name)

'''	
#use either on_message() OR .command
@bot.event 
async def on_message(message):
	#Make sure message isn't from our bot
	if message.author == bot.user:
		return
	
	if message.content == 'raise-exception':
		raise discord.DiscordException
	
	elif message.content == 'rand!':
		response = random.choice(randQuotes)
		await message.channel.send(response)
	
	elif 'happy birthday' in message.content.lower():
		await message.channel.send('Happy Birthday! :cake:')
'''	
	
@bot.event 
async def on_error(event, *args, **kwargs):
	with open('./err.log', 'a') as f:
		if event == 'on_message':
			print('Error')
			f.write(f'Unhandled message: {args[0]}\n\n')
		else:
			raise
	
bot.run(TOKEN)
