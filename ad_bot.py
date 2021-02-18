# bot.py
import os
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv

#bot setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()
bot = commands.Bot(command_prefix='!')
spammers = []

#bot logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="LA Tech Cyber Storm"))

@bot.event
async def on_message(message):
    #check if admin
    if message.author.guild_permissions.administrator:
        return
    #check if bot message
    if message.author == client.user:
        return
    await message.author.create_dm()
    #check if solution command
    if message.content.startswith("!solution"):
        await bot.process_commands(message)
    #otherwise spam
    #todo: kick member from channel after 3 spam messages (with 2 warnings prior) 
    else:
        spammers.append(message.author.name)
        for user in spammers:
            if user is message.author.name:
                if spammers.count(user) == 1:
                    await message.author.dm_channel.send("No spamming! (Warning)")
                elif spammers.count(user) == 2:
                    await message.author.dm_channel.send("No spamming! (Last warning)")
                elif spammers.count(user) >= 3:
                    await message.author.dm_channel.send("I warned you!")
                    #print(message.author)
                    #for guild in client.guilds:
                    #    print(message.author)
                    #    if guild.name == GUILD:
                    await member.kick(message.author)

    #remove sent message
    await message.delete()

@bot.command()
async def solution(ctx, *, arg):
    #check channel and solution
    #todo: add message author to new channel/role
    if ctx.channel.name == "general" and arg == "test":
        await ctx.author.dm_channel.send("Correct! You have been added to the next channel.")
    else:
        await ctx.author.dm_channel.send("Solution is incorrect. Please try again.")

bot.run(TOKEN)
