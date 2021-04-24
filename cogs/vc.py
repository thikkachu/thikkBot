#some code from joek13 forked here (tysm for existing!)

import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from urllib3 import request
import random
import os
import youtube_dl
import asyncio
#-----------------------YDL STUFF-----------------------#
YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}

async def ifPlaying(ctx):
    voice = ctx.guild.voice_client
    if voice and voice.channel and voice.source:
        return True
    else:
        raise commands.CommandError("No audio playing")

class Video:

    def __init__(self, url_or_search, requested_by):
        """Plays audio from (or searches for) a URL."""
        with youtube_dl.YoutubeDL(YTDL_OPTS) as ydl:
            video = self._get_info(url_or_search)
            video_format = video["formats"][0]
            self.stream_url = video_format["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.uploader = video["uploader"] if "uploader" in video else ""
            self.thumbnail = video[
                "thumbnail"] if "thumbnail" in video else None
            self.requested_by = requested_by

    def _get_info(self, video_url):
        with youtube_dl.YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][0]["url"])  # get info for first video
            else:
                video = info
            return video

    def get_embed(self):
        """Makes an embed out of this Video's information."""
        embed = discord.Embed(
            title=self.title, description=self.uploader, url=self.video_url)
        embed.set_footer(
            text=f"Requested by {self.requested_by.name}",
            icon_url=self.requested_by.avatar_url)
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        return embed


async def audio_playing(self, ctx):
# """Checks that audio is currently playing before continuing."""
    voice = ctx.guild.voice_client
    if thikka and thikka.channel and thikka.source:
        return True
    else:
        raise commands.CommandError("Not currently playing any audio.")

async def in_voice_channel(ctx):
    """Checks that the command sender is in the same voice channel as the bot."""
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel:
        return True
    else:
        raise commands.CommandError("You need to be in the channel to do that.")

async def is_audio_requester(ctx):
    """Checks that the command sender is the song requester."""
    music = ctx.bot.get_cog("vc")
    state = music.get_state(ctx.guild)
    permissions = ctx.channel.permissions_for(ctx.author)
    if permissions.administrator or state.is_requester(ctx.author):
        return True
    else:
        raise commands.CommandError("You need to be the song requester to do that.")

#-----------------------YDL STUFF-----------------------#


class vc(commands.Cog):
#-------------------------INITIALIZES COG ENV-----------------------------#

    def __init__ (self, thikka):
        self.thikka = thikka
        self.states = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('VC cog loaded successfully')
    
    def get_state(self, guild):
        """Gets the state for `guild`, creating it if it does not exist."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

#-------------------------/INITIALIZES COG ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------# 

    def _play_song(self, client, state, song):
        state.now_playing = song
        state.skip_votes = set()  # clear skip votes
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url), volume=state.volume)

        async def after_playing(err):
            if len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                self._play_song(client, state, next_song)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(),self.bot.loop)

        client.play(source, after=after_playing)
    
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
    @commands.guild_only()
    async def skip(self,ctx, *, misc = ''):
        voice = ctx.guild.voice_client
        voice.stop()


    
    @commands.command(aliases = ['np'])
    @commands.guild_only()
    @commands.check(ifPlaying)
    @commands.check(in_voice_channel)
    async def nowplaying(self, ctx):
        state = self.thikka.get_state(ctx.guild)
        await ctx.send('', embed = state.now_playing.get_embed())
    @nowplaying.error
    async def np_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send('**Nothing** playing dumbass.')

    @commands.command(aliases = ['add'])
    async def play(self, ctx, url : str, *, misc =''): #plays music using ffmpeg and ydl
        # if ctx.voice_client is None:
        #     await channel.connect()
        # if (voice.is_playing()) or (voice.is_paused()):
        #     await ctx.send(f'**{toPlay.title}** added to queue.')
        #     return
        voice = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        
        
        if voice and voice.channel:
            try:
                vid = Video(url, ctx.author)
            except youtube_dl.DownloadError as e:
                await ctx.send(f"Unable to download {e}. :flushed:")
                return
            state.playlist.append(vid)
            await ctx.send(f"Queued:", embed=vid.get_embed())

        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                try:
                    vid = Video(url, ctx.author)
                except youtube_dl.DownloadError as e:
                    await ctx.send(
                        "There was an error downloading your video, sorry.")
                    return
                client = await channel.connect()
                self._play_song(client, state, vid)
                await ctx.send("", embed=vid.get_embed())
            else:
                raise commands.CommandError("You need to be in a voice channel to do that.")
        # async with ctx.typing():
        #     toPlay = await YTDLSource.from_url(queue[0], loop = self.thikka.loop())
        #     voice.play(toPlay, after = lambda e: print(f'Error: %s' % e) if e else None)
        
        # if (not voice.is_playing()) or (not voice.is_paused()):
        #     await ctx.send(f'**Playing:** {toPlay.title}')
        
        # del(queue[0])
        

    # @play.error #error handler for play command 
    # async def play_error(self, ctx, error):
    #     if isinstance(error, commands.CommandInvokeError):
    #         if str(error).startswith('Command raised an exception: ClientException: Already connected to a voice channel.'):
    #             await ctx.send("I'm already connected to a voice channel stupid.")
    #         elif str(error).startswith("Command raised an exception: AttributeError: 'NoneType' object has no attribute 'channel'"):
    #             await ctx.send("You're not connected to a voice channel dum dum.")

    
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

class GuildState:

    def __init__(self):
        self.volume = 1.0
        self.playlist = []
        self.skip_votes = set()
        self.now_playing = None

    def is_requester(self, user):
        return self.now_playing.requested_by == user

def setup(thikka): #integrates cog into main.py
    thikka.add_cog(vc(thikka))

