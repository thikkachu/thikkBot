#made by thikkachu.

import discord
from discord.ext import commands
import random
import json
import os

#-------------------------INITIALIZES BOT ENV-----------------------------#

thikka = commands.Bot(command_prefix='^')
with open ("cogs/speech.json") as file:
    data = json.load(file)
with open ("key.json") as file:
    key = json.load(file)
@thikka.event
async def on_ready():
    print("{0.user} ready".format(thikka))
    await thikka.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="my life go down the drain '^help'"))
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        thikka.load_extension(f'cogs.{file[:-3]}')

#-------------------------/INITIALIZES BOT ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------#

#---------cog management area--------#
@thikka.command() #loads cog file
async def load(ctx, ext = "placeholder"):
    if ext == "placeholder":
        await ctx.send("Syntax: `^load (cog name)`")
    if (str(ctx.author.id) == "334245365148549120") or (str(ctx.author.id) == '198285838247919616'): 
        thikka.load_extension(f'cogs.{ext}')
        await ctx.send(f'`{ext}` loaded successfully')
    else:
        await ctx.send('fuck off cunt')
@thikka.command() #unloads cog file
async def unload(ctx, ext = "placeholder"):
    if ext == "placeholder":
        await ctx.send("Syntax: `^unload (cog name)`")
    elif (str(ctx.author.id) == "334245365148549120") or (str(ctx.author.id) == '198285838247919616'): 
        thikka.unload_extension(f'cogs.{ext}')
        await ctx.send(f'`{ext}` unloaded successfully')
    else:
        await ctx.send('fuck off cunt')
@thikka.command() #reloads cog file
async def reload(ctx, ext = "placeholder"):
    if ext == "placeholder":
        await ctx.send("Syntax: `^reload (cog name)`")
    elif (str(ctx.author.id) == "334245365148549120") or (str(ctx.author.id) == '198285838247919616'):       
        thikka.unload_extension(f'cogs.{ext}')
        thikka.load_extension(f'cogs.{ext}')
        await ctx.send(f'`{ext}` reloaded successfully')
    else:
        await ctx.send('fuck off cunt')
#---------/cog management area--------#

#------------------------------/COMMANDS AREA------------------------------#


#-------------------------JOIN/LEAVE MESSAGE AREA-------------------------#

@thikka.event
async def on_member_join(member):
    print(f'{member} is here to waste their life')

@thikka.event
async def on_member_remove(member):
    print(f'{member} is gone')

#-------------------------/JOIN/LEAVE MESSAGE AREA-------------------------#

thikka.run(key['key'])