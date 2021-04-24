#made by thikkachu.

import discord
from discord.ext import commands, tasks
import random
import json
import os
import asyncio

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

@thikka.command(aliases = ['', ' ']) #returns a message whenever ^ prefix is used without an arg
async def _blank(ctx, *, misc = ''):
    await ctx.send('Maybe try making a coherent sentence before summoning me.\n`^help to get started`')

#---------cog management area--------#

@thikka.command() #loads cog file
async def load(ctx, ext = "placeholder"):
    if ext == "placeholder":
        await ctx.send("Syntax: `^load (cog name)`")
    if (str(ctx.author.id) == "334245365148549120") or (str(ctx.author.id) == '198285838247919616'): 
        thikka.load_extension(f'cogs.{ext}')
        await ctx.send(f'`{ext}` loaded successfully')
        print(f'`{ext}` cog loaded successfully')
    else:
        await ctx.send('fuck off cunt')
@thikka.command() #unloads cog file
async def unload(ctx, ext = "placeholder"):
    if ext == "placeholder":
        await ctx.send("Syntax: `^unload (cog name)`")
    elif (str(ctx.author.id) == "334245365148549120") or (str(ctx.author.id) == '198285838247919616'): 
        thikka.unload_extension(f'cogs.{ext}')
        await ctx.send(f'`{ext}` unloaded successfully')
        print(f'`{ext}` cog unloaded successfully')
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
        print(f'`{ext}` cog reloaded successfully')
    else:
        await ctx.send('fuck off cunt')

#---------/cog management area--------#

#------------------------------/COMMANDS AREA------------------------------#


#-------------------------EVENTS AREA-------------------------#

# @thikka.event #global error handler
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.BadArgument):
#         await ctx.send("I don't know how you did it, but you fucked up cause I can't process this shit. **('Bad Argument')**")
#     elif isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("You're missing some pieces of the puzzle buckaroo. **('Missing Required Argument')**")
#     elif isinstance(error, commands.CommandNotFound):
#         await ctx.send("That command doesn't exist you absolute melon.")
#     elif isinstance(error, commands.MissingPermissions):
#         await ctx.send("**YOU** need **MY** permission to run that command. :angry:")
#     else:
#         print(error)

@thikka.event
async def on_member_join(member):
    print(f'{member} is here to waste their life')

@thikka.event
async def on_member_remove(member):
    print(f'{member} is gone')

#-------------------------/EVENTS AREA-------------------------#

thikka.run(key['key'])