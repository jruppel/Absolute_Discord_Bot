# bot.py
import os
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv

#bot setup
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')
spammers = []
commands = ["!solution", "!register", "!jointeam", "!reset"]

#bot logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Cyberstorm"))

@bot.event
async def on_message(message):
    global commands
    
    #check if bot message
    if message.author == client.user:
        return
    #allow messages within Teams category
    if message.channel.category.name == "Teams":
        return
    
    await message.author.create_dm()
    
    #check if command
    if message.content.split(" ")[0] in commands:
        await bot.process_commands(message)
        
    #otherwise spam
    #todo: kick member from channel after 3 spam messages (with 2 warnings prior) 
    else:
        await message.author.dm_channel.send(message.content)
        #check if admin
        if message.author.guild_permissions.administrator:
            return
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

    guild = ctx.author.guild
    level1 = discord.utils.get(guild.roles, name="Level 1")
    level2 = discord.utils.get(guild.roles, name="Level 2")
    level3 = discord.utils.get(guild.roles, name="Level 3")
    level4 = discord.utils.get(guild.roles, name="Level 4")
    level5 = discord.utils.get(guild.roles, name="Level 5")
    winners = discord.utils.get(guild.text_channels, name="winners")

    for r in guild.roles:
        if r.name in [y.name for y in ctx.author.roles]:
            if not ("Level" in r.name or r.name == "Admin" or r.name == "@everyone"):
                team = discord.utils.get(guild.roles, name=r.name)
                print(team)
    
    #check channel and solution
    #todo: add message author to new channel/role
    if ctx.channel.category.name == "Levels":
        if arg == "test":
            if "Level 1" in [y.name for y in ctx.author.roles]:
                await ctx.author.remove_roles(level1)
                await ctx.author.add_roles(level2)
            elif "Level 2" in [y.name for y in ctx.author.roles]:
                await ctx.author.remove_roles(level2)
                await ctx.author.add_roles(level3)
            elif "Level 3" in [y.name for y in ctx.author.roles]:
                await ctx.author.remove_roles(level3)
                await ctx.author.add_roles(level4)
            elif "Level 4" in [y.name for y in ctx.author.roles]:
                await ctx.author.remove_roles(level4)
                await ctx.author.add_roles(level5)
            elif "Level 5" in [y.name for y in ctx.author.roles]:
                await ctx.author.remove_roles(level5)
                await winners.set_permissions(team, view_channel=True)
                
        # do other stuff
            await ctx.author.dm_channel.send("Correct! Proceed to the next level.")
        else:
            await ctx.author.dm_channel.send("Incorrect. Try again.")
    else:
        await ctx.author.dm_channel.send("This isn't the right area to submit your solution.")

@bot.command()
async def register(ctx, *, arg):
    if ctx.channel.name == "welcome":
        guild = ctx.author.guild
        teams_category = discord.utils.get(ctx.guild.channels, name="Teams")
        team_channel = discord.utils.get(guild.text_channels, name=arg.replace(" ", "-"))
        team_role = discord.utils.get(guild.roles, name=arg.title())
        level1_role = discord.utils.get(guild.roles, name="Level 1")

        for r in guild.roles:
            if r.name in [y.name for y in ctx.author.roles]:
                if not ("Level" in r.name or r.name == "Admin" or r.name == "@everyone"):
                    team = discord.utils.get(guild.roles, name=r.name)
                    await ctx.author.dm_channel.send("You are not allowed to create a different team. If you joined the wrong team or this is a bug, contact an Admin.")
                    return
                else:
                    if team_channel is None:
                        teams_category = discord.utils.get(ctx.guild.channels, name="Teams")
                        team_channel = await guild.create_text_channel(arg, category=teams_category)    
                        
                        await team_channel.set_permissions(guild.default_role, read_message_history=False, send_messages=False, create_instant_invite=False)
                        
                        if team_role is None:
                            team_role = await guild.create_role(name=arg.title(), colour=discord.Colour(0xffd700))
                            await team_channel.set_permissions(team_role, read_message_history=True, send_messages=True)
                            await team_channel.send("Use `!solution` to submit your answer to the Puzzlemaster.\n\nEverything is allowed when doing these challenges and no code should be left behind!\n\nGood luck! :four_leaf_clover:")
                            await ctx.author.add_roles(team_role)
                            await ctx.author.dm_channel.send(f"Successfully created team {arg.title()}")
                            await ctx.author.add_roles(level1_role)
                        else:
                            await ctx.author.dm_channel.send("The team you tried to register already exists. Use !jointeam to join.")
    else:
        return

@bot.command()
async def jointeam(ctx, *, arg):
    if ctx.channel.name == "welcome":
        guild = ctx.author.guild
        team_channel = discord.utils.get(guild.text_channels, name=arg.replace(" ", "-"))
        
        for r in guild.roles:
            if r.name in [y.name for y in ctx.author.roles]:
                if not ("Level" in r.name or r.name == "Admin" or r.name == "@everyone"):
                    team = discord.utils.get(guild.roles, name=r.name)
                    await ctx.author.dm_channel.send("You are not allowed to join a different team. If you joined the wrong team or this is a bug, contact an Admin.")
                    return
                else:
                    if team_channel is None:
                        await ctx.author.dm_channel.send("The team you tried to join does not exist. Did you type the name correctly?")
                    else:
                        role = discord.utils.get(guild.roles, name=arg.title())
                        await ctx.author.add_roles(role)
                        await ctx.author.dm_channel.send(f"Successfully joined team {arg.title()}")
    else:
        return

bot.run(TOKEN)
