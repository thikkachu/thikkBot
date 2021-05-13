import discord
import logging
import sys
from discord.enums import _is_descriptor
import toml
from discord.ext import commands
from .cogs import math,music, error, meta, tips, fun, gambling, serverManagement
from . import config

cfg = config.load_config()

bot = commands.Bot(command_prefix=cfg["prefix"], case_insensitive=True)
bot.remove_command('help')

#---------------------------HELP-CMD----------------------------#

@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title = "Help", description = "^help <command> for more info on that command.")
    embed.add_field(name="Fun", value = "thikk, cat, sex")
    embed.add_field(name="Music", value = "play, pause, leave, volume, skip, loop, nowplaying, queue, clearqueue, jumpqueue, remove")
    embed.add_field(name="Gambling / Luck", value = "rolld, roll, coin")
    embed.add_field(name="Moderator", value = "ping, clear")
    embed.add_field(name="Miscellaneous", value = "uptime, tip")
    embed.add_field(name="Under Development", value = "D&D Commands, Math Stuff, Neural Network, Spotify API Integ.")
    await ctx.send(embed = embed)

@help.command()
async def thikk(ctx):
    embed = discord.Embed(title = "^thikk", description = "Sends a very nice message back at you! Or a custom message if you're special.")
    embed.add_field(name = "**Command Syntax**", value = "^thikk")
    await ctx.send(embed=embed)
@help.command()
async def cat(ctx):
    embed = discord.Embed(title = "^cat", description = "Sends a random picture of my cat. There are two exceedingly rare cat rolls!")
    embed.add_field(name = "**Command Syntax**", value = "^cat")
    await ctx.send(embed=embed)
@help.command()
async def sex(ctx):
    embed = discord.Embed(title = "^sex", description = "ƎNA decides for you whether or not sex.")
    embed.add_field(name = "**Command Syntax**", value = "^sex")
    await ctx.send(embed=embed)
@help.command()
async def play(ctx):
    embed = discord.Embed(title = "Music: ^play", description = "Plays a song from the given URL or searches for a song from your input, and plays it in your voice channel.")
    embed.add_field(name = "**Command Syntax**", value = "^play <url/searchterms>")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^p   ^pl   ^pla")
    await ctx.send(embed=embed)
@help.command()
async def pause(ctx):
    embed = discord.Embed(title = "Music: ^pause", description = "Pauses/Resumes Song")
    embed.add_field(name = "**Command Syntax**", value = "^pause")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^resume")
    await ctx.send(embed=embed)
@help.command()
async def leave(ctx):
    embed = discord.Embed(title = "Music: ^stop", description = "Makes bot stop playing music and leave the voice channel it's in.")
    embed.add_field(name = "**Command Syntax**", value = "^stop")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^leave")
    await ctx.send(embed=embed)
@help.command()
async def volume(ctx):
    embed = discord.Embed(title = "Music: ^volume", description = "Changes music volume. MAX: `250`")
    embed.add_field(name = "**Command Syntax**", value = "^volume <# out of 250>")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^v   ^vol")
    await ctx.send(embed=embed)
@help.command()
async def skip(ctx):
    embed = discord.Embed(title = "Music: ^skip", description = "Skips current song.")
    embed.add_field(name = "**Command Syntax**", value = "^skip")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^s   ^sk")
    await ctx.send(embed=embed) 
@help.command()
async def loop(ctx):
    embed = discord.Embed(title = "Music: ^loop", description = "Loops current song.")
    embed.add_field(name = "**Command Syntax**", value = "^loop")
    await ctx.send(embed=embed) 
@help.command()
async def nowplaying(ctx):
    embed = discord.Embed(title = "Music: ^nowplaying", description = "Displays what song is currently playing.")
    embed.add_field(name = "**Command Syntax**", value = "^nowplaying")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^np")
    await ctx.send(embed=embed) 
@help.command()
async def queue(ctx):
    embed = discord.Embed(title = "Music: ^queue", description = "Displays the upcoming song list.")
    embed.add_field(name = "**Command Syntax**", value = "^queue")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^q   ^playlist")
    await ctx.send(embed=embed) 
@help.command()
async def clearqueue(ctx):
    embed = discord.Embed(title = "Music: ^clearqueue", description = "Clears the upcoming song queue.")
    embed.add_field(name = "**Command Syntax**", value = "^clearqueue")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^cq")
    await ctx.send(embed=embed) 
@help.command()
async def jumpqueue(ctx):
    embed = discord.Embed(title = "Music: ^nowplaying", description = "Switches queue position of 2 songs")
    embed.add_field(name = "**Command Syntax**", value = "^jumpqueue <Queue Position 1> <Queue Position 2>")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^jq")
    await ctx.send(embed=embed) 
@help.command()
async def remove(ctx):
    embed = discord.Embed(title = "Music: ^remove", description = "Removes song from upcoming song queue.")
    embed.add_field(name = "**Command Syntax**", value = "^remove <Queue Position>")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^rm")
    await ctx.send(embed=embed) 
@help.command()
async def rolld(ctx):
    embed = discord.Embed(title = "Gambling: ^rolld", description = "Rolls die/dice using the d&d syntax.")
    embed.add_field(name = "**Command Syntax**", value = "^rolld <times>d<sides> (rolls a d20 by default)")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^droll")
    await ctx.send(embed=embed) 
@help.command()
async def roll(ctx):
    embed = discord.Embed(title = "Gambling: ^roll", description = "Rolls die/dice")
    embed.add_field(name = "**Command Syntax**", value = "^rolld <sides> <times> (rolls a 6 sided die by default)")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^die   ^dice")
    await ctx.send(embed=embed) 
@help.command()
async def coin(ctx):
    embed = discord.Embed(title = "Gambling: ^coin", description = "Flips coin(s)")
    embed.add_field(name = "**Command Syntax**", value = "^rolld <times>d<sides>")
    embed.add_field(name="Command Shortcuts/Aliases", value = "^coinflip   ^flip")
    await ctx.send(embed=embed)
@help.command()
async def ping(ctx):
    embed = discord.Embed(title = "Moderation: ^ping", description = "Checks bot latency.")
    embed.add_field(name = "**Command Syntax**", value = "^ping")
    await ctx.send(embed=embed)
@help.command()
async def clear(ctx):
    embed = discord.Embed(title = "Moderation: ^clear", description = "Purges messages from channel.")
    embed.add_field(name = "**Command Syntax**", value = "^clear <amount> (deletes 10 messages by default) (^clear all to delete 100 or all.OverrideLimit to delete everything)")
    await ctx.send(embed=embed)
@help.command()
async def uptime(ctx):
    embed = discord.Embed(title = "Miscellaneous: ^uptime", description = "Checks bot's uptime.")
    embed.add_field(name = "**Command Syntax**", value = "^uptime")
    await ctx.send(embed=embed)
@help.command()
async def tip(ctx):
    embed = discord.Embed(title = "Miscellaneous: ^tip", description = "Nothing yet.")
    embed.add_field(name = "**Command Syntax**", value = "^tip")
    await ctx.send(embed=embed)

#---------------------------HELP-CMD----------------------------#

@bot.event 
async def on_ready():
    logging.info(f"Logged in as {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="my life go down the drain '^help'"))

COGS = [music.Music, error.CommandErrorHandler, meta.Meta, tips.Tips, gambling.Gambling, fun.fun, serverManagement.serverManagement, math.math]


def add_cogs(bot):
    for cog in COGS:
        bot.add_cog(cog(bot, cfg))  # Initialize the cog and add it to the bot


def run():
    add_cogs(bot)
    if cfg["token"] == "":
        raise ValueError(
            "No token has been provided. Please ensure that config.toml contains the bot token."
        )
        sys.exit(1)
    bot.run(cfg["token"])
