import discord
from discord.ext import commands, tasks
import random
import os
import youtube_dl

class vc(commands.Cog):
#-------------------------INITIALIZES COG ENV-----------------------------#

    def __init__ (self, thikka):
        self.thikka = thikka

    @commands.Cog.listener()
    async def on_ready(self):
        print('VC cog loaded successfully')

#-------------------------/INITIALIZES COG ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------# 

    @commands.command(aliases = ['connect']) #connects to channel user is connected to
    async def join(self, ctx, *, misc = ''):
        channel = ctx.author.voice.channel
        await channel.connect()
    @join.error #error handler for join command 
    async def join_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if str(error).startswith('Command raised an exception: ClientException: Already connected to a voice channel.'):
                await ctx.send("I'm already connected to a voice channel stupid.")
            elif str(error).startswith("Command raised an exception: AttributeError: 'NoneType' object has no attribute 'channel'"):
                await ctx.send("You're not connected to a voice channel dum dum.")
    
    
    @commands.command(aliases = ['disconnect']) #disconnects bot from any vc it's in within the guild
    async def leave(self, ctx, *, misc = ''):
        channel = ctx.message.guild.voice_client
        if channel is None:
            return await ctx.send("Im not connected dumbass.")
        else:
            await channel.disconnect()

    @commands.command()
    async def play(self, ctx, url : str , *, misc =''): #plays music using ffmpeg and ydl
        song = os.path.isfile('song.mp3')
        try:
            if song:
                os.remove('song.mp3')
        except PermissionError:
            await ctx.send("There's still a song playing but my queue system isn't ready yet!\nPlease ^stop the currently playing audio or wait for it to end.")
        
        channel = ctx.author.voice.channel
        if not ctx.voice_client is not None:
            await channel.connect()
        voice = ctx.message.guild.voice_client
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio('song.mp3'))
        

    @play.error #error handler for play command 
    async def play_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if str(error).startswith('Command raised an exception: ClientException: Already connected to a voice channel.'):
                await ctx.send("I'm already connected to a voice channel stupid.")
            elif str(error).startswith("Command raised an exception: AttributeError: 'NoneType' object has no attribute 'channel'"):
                await ctx.send("You're not connected to a voice channel dum dum.")

    
    @commands.command() #pauses currently playing audio
    async def pause(self, ctx, *, misc = ''):
        channel = ctx.message.guild.voice_client
        if channel is None:
            return await ctx.send("How tf are you gonna try to pause when I'm not even connected to a vc? :disappointed:")
        if channel.is_playing():
            channel.pause()
        else:
            await ctx.send("There is no audio playing poopass.")
    
    @commands.command(aliases = ['go', 'continue']) #resumes paused audio
    async def resume(self, ctx, *, misc = ''):
        channel = ctx.message.guild.voice_client
        if channel is None:
            return await ctx.send("How tf are you gonna try to resume when I'm not even connected to a vc? :disappointed:")
        if channel.is_paused():
            channel.resume()
        else:
            await ctx.send("The audio isn't paused small cranium.")

    @commands.command(aliases = ['stop ']) #stops and unqueues currently playing audio
    async def stop(self, ctx, *, misc = ''):
        channel = ctx.message.guild.voice_client
        if channel is None:
            return await ctx.send("Stop?, STOP WHAT?. Make sure I'm in a vc before you try this again elephantitis looking ass.")
        else:
            channel.stop()

#------------------------------/COMMANDS AREA------------------------------#

def setup(thikka): #integrates cog into main.py
    thikka.add_cog(vc(thikka))