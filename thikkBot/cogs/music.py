from discord.ext import commands, tasks
import discord
import asyncio
import youtube_dl
import logging
import math
import time
from urllib import request
from ..video import Video


async def audio_playing(ctx):
    """Checks that audio is currently playing before continuing."""
    client = ctx.guild.voice_client
    if client and client.channel and client.source:
        return True
    else:
        raise commands.CommandError("I'm not playing anything poopass")


async def in_voice_channel(ctx):
    """Checks that the command sender is in the same voice channel as the bot."""
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel:
        return True
    else:
        raise commands.CommandError(
            "You're **not even in a channel!** What the fuck are you expecting out of me?")


async def is_audio_requester(ctx):
    """Checks that the command sender is the song requester."""
    music = ctx.bot.get_cog("Music")
    state = music.get_state(ctx.guild)
    permissions = ctx.channel.permissions_for(ctx.author)
    if permissions.administrator or state.is_requester(ctx.author):
        return True
    else:
        raise commands.CommandError(
            "You need to be the song requester to do that.")
loop = False

class Music(commands.Cog):
    """Bot commands to help play music."""

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config[__name__.split(".")[
            -1]]  # retrieve module name, find config entry
        self.states = {}
        # self.bot.add_listener(self.on_reaction_add, "on_reaction_add")

    def get_state(self, guild):
        """Gets the state for `guild`, creating it if it does not exist."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    @commands.command(aliases=["stop"])
    @commands.guild_only()
    async def leave(self, ctx):
        """Leaves the voice channel, if currently in one."""
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        if client and client.channel:
            await client.disconnect()
            state.playlist = []
            state.now_playing = None
        else:
            raise commands.CommandError("Not in a channel smallcock.")

    @commands.command(aliases=["resume"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def pause(self, ctx):
        """Pauses any currently playing audio."""
        client = ctx.guild.voice_client
        self._pause_audio(client)

    def _pause_audio(self, client):
        if client.is_paused():
            client.resume()
        else:
            client.pause()
    

    @commands.command(aliases=["vol", "v"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def volume(self, ctx, volume: int):
        """Change the volume of currently playing audio (values 0-250)."""
        state = self.get_state(ctx.guild)

        # make sure volume is nonnegative
        if volume < 0:
            volume = 0

        max_vol = self.config["max_volume"]
        if max_vol > -1:  # check if max volume is set
            # clamp volume to [0, max_vol]
            if volume > max_vol:
                volume = max_vol

        client = ctx.guild.voice_client

        state.volume = float(volume) / 100.0
        client.source.volume = state.volume  # update the AudioSource's volume to match

    @commands.command(aliases = ['s', 'sk'])
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def skip(self, ctx): #skips current song
        state = self.get_state(ctx.guild)
        client = ctx.guild.voice_client
        client.stop()

    def _play_song(self, client, state, song, msg):
        ffmpeg_options = {
        'options': '-vn',
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        }
        state.now_playing = song
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url, **ffmpeg_options), volume=state.volume)

        def after_playing(err):
            global loop
            if loop == True:
                self._play_song(client, state, song, msg)
            elif len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                self._play_song(client, state, next_song, msg)
                asyncio.run_coroutine_threadsafe(msg.send(f"**Now playing** {next_song.title}", embed=next_song.get_embed()) ,self.bot.loop)



        client.play(source, after=after_playing)
    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    async def loop(self, ctx, *, misc = ''):
        global loop
        if loop == False:
            loop = True
            await ctx.send("I'm gonna loop this dick around your asshole boy. (now looping current song)")
        elif loop == True:
            loop = False
            await ctx.send("Looping disabled, heterosexuality re-established.")

    @commands.command(aliases=["np"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def nowplaying(self, ctx):
        """Displays information about the current song."""
        state = self.get_state(ctx.guild)
        message = await ctx.send("", embed=state.now_playing.get_embed())

    @commands.command(aliases=["q", "playlist"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def queue(self, ctx):
        """Display the current play queue."""
        state = self.get_state(ctx.guild)
        await ctx.send(self._queue_text(state.playlist))

    def _queue_text(self, queue):
        """Returns a block of text describing a given song queue."""
        if len(queue) > 0:
            message = [f"{len(queue)} in queue:"]
            message += [
                f"  {index+1}. **{song.title}** (requested by **{song.requested_by.name}**)"
                for (index, song) in enumerate(queue)
            ]  # add individual songs
            return "\n".join(message)
        else:
            return "Your time is running short young one, there's **nothing** left in the queue. :eggplant:"

    @commands.command(aliases=["cq"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def clearqueue(self, ctx):
        """Clears the play queue without leaving the channel."""
        state = self.get_state(ctx.guild)
        state.playlist = []

    @commands.command(aliases=["jq"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def jumpqueue(self, ctx, song: int, new_index: int):
        """Moves song at an index to `new_index` in queue."""
        state = self.get_state(ctx.guild)  # get state for this guild
        if 1 <= song <= len(state.playlist) and 1 <= new_index:
            song = state.playlist.pop(song - 1)  # take song at index...
            state.playlist.insert(new_index - 1, song)  # and insert it.

            await ctx.send(self._queue_text(state.playlist))
        else:
            raise commands.CommandError("You must use a valid index.")

    @commands.command(brief="Plays audio from <url>.", aliases = ['p', 'pl', 'pla'])
    @commands.guild_only()
    async def play(self, ctx, *, url):
        """Plays audio hosted at <url> (or performs a search for <url> and plays the first result)."""

        client = ctx.guild.voice_client
        msg = ctx
        state = self.get_state(ctx.guild)  # get the guild's state

        if client and client.channel:
            try:
                video = Video(url, ctx.author)
            except youtube_dl.DownloadError as e:
                logging.warn(f"Error downloading video: {e}")
                await ctx.send(
                    "There was an error downloading your video, sorry.")
                return
            state.playlist.append(video)
            message = await ctx.send(
                "Added to queue.", embed=video.get_embed())
        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                try:
                    video = Video(url, ctx.author)
                except youtube_dl.DownloadError as e:
                    await ctx.send(
                        "There was an error downloading your video, sorry.")
                    return
                client = await channel.connect()
                self._play_song(client, state, video, msg)
                message = await ctx.send("**Now playing:**", embed=video.get_embed())
                logging.info(f"Now playing '{video.title}'")
            else:
                raise commands.CommandError(
                    "You're not in a vc dumbass")

    @tasks.loop(seconds=180)
    async def voice_check(self, ctx):
        client = ctx.guild.voice_client
        if client.is_playing():
            return
        elif not client.is_playing():
            await client.disconnect()



class GuildState:
    """Helper class managing per-guild state."""

    def __init__(self):
        self.volume = 1.0
        self.playlist = []
        self.now_playing = None

    def is_requester(self, user):
        return self.now_playing.requested_by == user
