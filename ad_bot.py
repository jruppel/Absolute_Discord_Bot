# bot.py
import os
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get

#bot setup
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')
spammers = []
commands = ["!solution", "!register", "!jointeam", "!deleteteam", "!reset"]

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
    await message.author.create_dm()

    #check if command
    if message.content.split(" ")[0] in commands:
        await bot.process_commands(message)
            
##        #otherwise spam
##        #todo: kick member from channel after 3 spam messages (with 2 warnings prior) 
##        else:
##            await message.author.dm_channel.send(message.content)
##            #check if admin
##            if message.author.guild_permissions.administrator:
##                return
##            spammers.append(message.author.name)
##            for user in spammers:
##                if user is message.author.name:
##                    if spammers.count(user) == 1:
##                        await message.author.dm_channel.send("No spamming! (Warning)")
##                    elif spammers.count(user) == 2:
##                        await message.author.dm_channel.send("No spamming! (Last warning)")
##                    elif spammers.count(user) >= 3:
##                        await message.author.dm_channel.send("I warned you!")
##                        #print(message.author)
##                        #for guild in client.guilds:
##                        #    print(message.author)
##                        #    if guild.name == GUILD:
##                        await member.kick(message.author)
    if message.channel.name == "welcome":
        await message.delete()

@bot.command()
async def solution(ctx, *, arg):
    
    guild = ctx.author.guild
    
    level1 = get(guild.roles, name="Level 1")
    level2 = get(guild.roles, name="Level 2")
    level3 = get(guild.roles, name="Level 3")
    level4 = get(guild.roles, name="Level 4")
    level5 = get(guild.roles, name="Level 5")

    level1_channel = get(guild.text_channels, name="level-1")
    level2_channel = get(guild.text_channels, name="level-2")
    level3_channel = get(guild.text_channels, name="level-3")
    level4_channel = get(guild.text_channels, name="level-4")
    level5_channel = get(guild.text_channels, name="level-5")
    
    winners = get(guild.text_channels, name="winners")
    log_channel = get(guild.text_channels, name="log")

    for r in guild.roles:
        if r.name in [y.name for y in ctx.author.roles]:
            if not ("Level" in r.name or r.name == "Admin" or r.name == "@everyone"):
                team_name = r.name
                team = get(guild.roles, name=team_name)
                
    team_channel = get(guild.text_channels, name=team_name.replace(" ", "-").lower())
    
    #check channel and solution
    #todo: add message author to new channel/role
    if ctx.channel.category.name == "Teams":
        if "Level 1" in [y.name for y in ctx.author.roles]:
            if arg == "perseverance":
                await team_channel.send("**Correct!**")
                await team_channel.send("On to the next level! " + level2_channel.mention)
                await ctx.author.remove_roles(level1)
                await ctx.author.add_roles(level2)
                await log_channel.send(team_channel.mention + " leveled up to Level 2")
            else:
                await team_channel.send("Incorrect. Try again.")
                
        elif "Level 2" in [y.name for y in ctx.author.roles]:
            if arg == "answer2":
                await team_channel.send("**Correct!**")
                await team_channel.send("Nice! Here's the next level! :point_right: " + level3_channel.mention)
                await ctx.author.remove_roles(level2)
                await ctx.author.add_roles(level3)
                await log_channel.send(team_channel.mention + " leveled up to Level 3")
            else:
                await team_channel.send("Incorrect. Try again.")
                
        elif "Level 3" in [y.name for y in ctx.author.roles]:
            if arg == "answer3":
                await team_channel.send("**Correct!**")
                await team_channel.send("...didn't expect you to get that one... :sweat_smile: " + level4_channel.mention)
                await ctx.author.remove_roles(level3)
                await ctx.author.add_roles(level4)
                await log_channel.send(team_channel.mention + " leveled up to Level 4")
            else:
                await team_channel.send("Incorrect. Try again.")
                
        elif "Level 4" in [y.name for y in ctx.author.roles]:
            if arg == "answer4":
                await team_channel.send("**Correct!**")
                await team_channel.send("I wonder how many levels there are? :thinking::wink: " + level5_channel.mention)
                await ctx.author.remove_roles(level4)
                await ctx.author.add_roles(level5)
                await log_channel.send(team_channel.mention + " leveled up to Level 4")
            else:
                await team_channel.send("Incorrect. Try again.")
                
        elif "Level 5" in [y.name for y in ctx.author.roles]:
            if arg == "answer5":
                await team_channel.send("**Correct!**")
                await team_channel.send("I can't believe it... **YOU WON?!** But is it really over?" + winners.mention)
                await ctx.author.remove_roles(level5)
                await winners.set_permissions(team, view_channel=True)
                await log_channel.send(team_channel.mention + " has finished the challenge!")
            else:
                await team_channel.send("Incorrect. Try again.")
                
        else:
            await ctx.author.dm_channel.send("Error. Contact an Admin. User does not have a Level role.")
##        await ctx.author.team_channel.send("Correct! Proceed to the next level.")

    else:
        await ctx.author.dm_channel.send("This isn't the right area to submit your solution.")

@bot.command()
async def register(ctx, *, arg):
    if ctx.channel.name == "welcome":
        guild = ctx.author.guild
        teams_category = get(ctx.guild.channels, name="Teams")
        team_channel = get(guild.text_channels, name=arg.replace(" ", "-"))
        team_role = get(guild.roles, name=arg.title())
        level1_role = get(guild.roles, name="Level 1")
        level1_channel = get(guild.text_channels, name="level-1")

        for r in guild.roles:
            if r.name in [y.name for y in ctx.author.roles]:
                if not ("Level" in r.name or r.name == "Admin" or r.name == "@everyone"):
                    team = get(guild.roles, name=r.name)
                    await ctx.author.dm_channel.send("You are not allowed to create a different team. If you joined the wrong team or this is a bug, contact an Admin.")
                    return
                
        if team_channel is None:
            teams_category = get(ctx.guild.channels, name="Teams")
            team_channel = await guild.create_text_channel(arg, category=teams_category)
            
            await team_channel.set_permissions(guild.default_role, read_message_history=False, send_messages=False, create_instant_invite=False)
            
            if team_role is None:
                team_role = await guild.create_role(name=arg.title(), colour=discord.Colour(0xffd700))
                await team_channel.set_permissions(team_role, read_message_history=True, send_messages=True)
                await team_channel.send("Use `!solution` to submit your answer.\n\nEverything is allowed when doing these challenges and no code should be left behind!\n\nGood luck! :four_leaf_clover: " + level1_channel.mention)
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
        team_channel = get(guild.text_channels, name=arg.replace(" ", "-"))
        
        for r in guild.roles:
            if r.name in [y.name for y in ctx.author.roles]:
                if not ("Level" in r.name or r.name == "Admin" or r.name == "@everyone"):
                    team = get(guild.roles, name=r.name)
                    await ctx.author.dm_channel.send("You are not allowed to join a different team. If you joined the wrong team or this is a bug, contact an Admin.")
                    return
        if team_channel is None:
            await ctx.author.dm_channel.send("The team you tried to join does not exist. Did you type the name correctly?")
        else:
            role = get(guild.roles, name=arg.title())
            await ctx.author.add_roles(role)
            await ctx.author.dm_channel.send(f"Successfully joined team {arg.title()}")
    else:
        return

@bot.command()
async def deleteteam(ctx, *, arg):
    if ctx.channel.name == "dev":
        guild = ctx.author.guild
        team_channel = get(guild.text_channels, name=arg.replace(" ", "-"))
        team_role = get(guild.roles, name=arg.title())
        dev_channel = get(guild.text_channels, name="dev")

        await dev_channel.send(f"Deleting {team_channel.mention} & {team_role.mention}...")
        await team_channel.delete()
        await team_role.delete()
        await dev_channel.send("Done!")
    else:
        return

bot.run(TOKEN)
