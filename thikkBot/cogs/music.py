import enum
from discord.ext import commands
import discord
import asyncio
import youtube_dl
import logging
import time
from urllib import request
from ..video import Video
from ..deezer import Deezerfy
import tekore
import os


async def spotify(self, ctx, args):
    if args.__contains__('/track'):
        id = tekore.from_url(args) 
        track = await self.bot.spotify.track(id[1])
        title = track.name
        artist = track.artists[0].name
        return f'{title} {artist}'


    elif args.__contains__('/playlist'):
        await ctx.send("Playlists aren't supported yet. fuck off im a slow worker")
    else:
        await ctx.send ("Could not parse Spotify link :D")

def timeFormat(seconds):
    if seconds >= 3600:
        duration = time.strftime('%H:%M:%S', time.gmtime(seconds))
        if duration.startswith('0'):
            duration = duration[1:]
        return duration
    else:
        duration = time.strftime('%M:%S', time.gmtime(seconds))
        if duration.startswith('0'):
            duration = duration[1:]
        return duration

def timeLeft(state, client):
    duration = state.now_playing.get_duration()
    endTime = startTime + duration
    currentTime = time.time()
    if client.is_paused():
        return f'{timeFormat(pauseTime-startTime)} / {timeFormat(duration)}'
    else:
        return f'{timeFormat(currentTime-startTime)} / {timeFormat(duration)}'
def titleLengthCheck(str):
    if len(str) >= 37:
        return(f'{str[0:36]}...')
    else:
        return str

def _queue_text_(state, queue):
    fullLength = 0
    for index in range(len(queue)):
        fullLength += queue[index-1].get_duration()
    embed = discord.Embed(title = "Music Queue", description = f'**Playing:** {state.now_playing.title}\n\n**Queue Length:** `{timeFormat(fullLength)}`')
    songList = []
    songList += [f'{index+1}. **{titleLengthCheck(song.title)}**' for (index,song) in enumerate(queue)]
    songList = "\n".join(songList)
    embed.add_field(name = "Songs", value=songList)
    durationList=[]
    durationList += [f'{timeFormat(song.duration)}' for song in queue]
    durationList = "\n".join(durationList)
    embed.add_field(name = "Duration", value=durationList)
    requesterList=[]
    requesterList += [f'{song.requested_by.name}' for song in queue]
    requesterList = "\n".join(requesterList)
    embed.add_field(name = "Requester", value=requesterList)
    return embed

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
        self._pause_audio(client, ctx)

    def _pause_audio(self, client, ctx):
        global pauseTime
        if client.is_paused():
            client.resume()
            asyncio.run_coroutine_threadsafe(ctx.send(f"Track **Resumed**"), self.bot.loop)
            startTime = time.time()
            
        else:
            client.pause()
            asyncio.run_coroutine_threadsafe(ctx.send(f"Track **Paused**"),self.bot.loop)
            pauseTime=time.time()
            
    
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

    def spotify(self, client, state, song, msg):
        state.now_playing = song
        global loop
    
    def _play_song(self, client, state, song, msg):
        ffmpeg_options = {
        'options': '-vn',
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        }
        state.now_playing = song
        global loop
        global startTime
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url, **ffmpeg_options), volume=state.volume)
        def after_playing(err):
            if loop == True:
                self._play_song(client, state, song, msg)
            elif len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                if next_song.artist:
                    self._play_song_deez(client, state, next_song, msg)
                    asyncio.run_coroutine_threadsafe(msg.send(f"**Now playing** {next_song.title}", embed=next_song.get_embed()) ,self.bot.loop)
                else:
                    self._play_song(client, state, next_song, msg)
                    asyncio.run_coroutine_threadsafe(msg.send(f"**Now playing** {next_song.title}", embed=next_song.get_embed()) ,self.bot.loop)
            else: 
                client.disconnect()

        
        client.play(source, after=after_playing)
        startTime = time.time()
    def _play_song_deez(self, client, state, song, msg):
        state.now_playing = song
        global loop
        global startTime
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(source='/Users/fermioni/Code/Thikkbot/thikkBot/cogs/tempMusic/'+ song.title + '.mp3'), volume=state.volume)
        

        def after_playing(err):
            os.remove('/Users/fermioni/Code/Thikkbot/thikkBot/cogs/tempMusic/'+ song.title + '.mp3')
            os.remove('/Users/fermioni/Code/Thikkbot/thikkBot/cogs/tempMusic/'+ song.title + '.lrc')
            if loop == True:
                self._play_song(client, state, song, msg)
            elif len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                if hasattr(next_song, 'artist'):
                    self._play_song_deez(client, state, next_song, msg)
                    asyncio.run_coroutine_threadsafe(msg.send(f"**Now playing** {next_song.title}", embed=next_song.get_embed()) ,self.bot.loop)
                else:
                    self._play_song(client, state, next_song, msg)
                    asyncio.run_coroutine_threadsafe(msg.send(f"**Now playing** {next_song.title}", embed=next_song.get_embed()) ,self.bot.loop)
            else: 
                client.disconnect()

        client.play(source, after=after_playing)
        startTime = time.time()
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
        client = ctx.guild.voice_client
        embed = state.now_playing.get_embed()
        embed.add_field(name = "⠀", value=f'⧖ {timeLeft(state, client)}')
        if ctx.guild.voice_client.is_paused():
            message = await ctx.send("**Currently Paused:**", embed=embed)
        else:
            message = await ctx.send("**Now Playing:**", embed=embed)

    @commands.command(aliases=["q", "playlist"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def queue(self, ctx):
        """Display the current play queue."""
        
        state = self.get_state(ctx.guild)
        queue = state.playlist
        if len(state.playlist) > 0:
            await ctx.send(embed=_queue_text_(state, queue))
        else:
            await ctx.send("Your time is running out young one... there is **nothing** left in the queue <:no:799019895291379753>")

    @commands.command(aliases=["cq"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def clearqueue(self, ctx):
        """Clears the play queue without leaving the channel."""
        state = self.get_state(ctx.guild)
        state.playlist = []
        await ctx.send("Queue Cleared... How could you do this in good conscience, what did the queue ever do to you huh?")

    @commands.command(aliases=["jq"] )
    @commands.guild_only()
    @commands.check(audio_playing)
    async def jumpqueue(self, ctx, song: int, new_index: int):
        """Moves song at an index to `new_index` in queue."""
        state = self.get_state(ctx.guild)  # get state for this guild
        if 1 <= song <= len(state.playlist) and 1 <= new_index:
            song = state.playlist.pop(song - 1)  # take song at index...
            state.playlist.insert(new_index - 1, song)  # and insert it.
            queue = state.playlist

            await ctx.send(embed = _queue_text_(state, queue))
        else:
            raise commands.CommandError("You must use a valid index.")

    @commands.command(aliases=['rm'], brief="Removes song from queue by it's index.")
    @commands.guild_only()
    @commands.check(audio_playing)
    async def remove(self, ctx, index: int, *, misc=''):
        state = self.get_state(ctx.guild)
        if 1 <= index <= len(state.playlist):
            index = state.playlist.pop(index-1)
            queue = state.playlist
            
            await ctx.send(embed=_queue_text_(state, queue))
        else:
            raise commands.CommandError("Out of range dumbass.")

    @commands.command(aliases=['dl'], brief="Downloads a song off deezer.")
    @commands.guild_only()
    async def download(self, ctx, *, url):
        try:
            song = Deezerfy(url, ctx.author)
        except:
            await ctx.send("Error with CDN")
            return
        await ctx.send(embed=song.get_embed())
        await ctx.send(embed=song.embed128())
        await ctx.send(embed=song.embed256())
        await ctx.send(embed=song.embed320())
        await ctx.send(embed=song.embedflac())
        os.remove('/Users/fermioni/Code/Thikkbot/thikkBot/cogs/tempMusic/'+ song.title + '.mp3')
        os.remove('/Users/fermioni/Code/Thikkbot/thikkBot/cogs/tempMusic/'+ song.title + '.lrc')

    @commands.command(brief="Plays audio from <url>.", aliases = ['p', 'pl', 'pla'])
    @commands.guild_only()
    async def play(self, ctx, *, url):
        """Plays audio hosted at <url> (or performs a search for <url> and plays the first result)."""
        client = ctx.guild.voice_client
        msg = ctx
        state = self.get_state(ctx.guild)  # get the guild's state
        if client and client.channel:
            if url.endswith("on deezer") or url.__contains__("https://www.deezer.com/en/track/"):
                if url.endswith("on deezer"):
                    url = url[:-9] #splices off "on deezer"
                if url.__contains__("https://www.deezer.com/en/track/"):
                    url = url[32:]
                    url = url.split("?", 1)[0]
                if client.is_playing():
                    try:
                        video = Deezerfy(url, ctx.author)
                    except youtube_dl.DownloadError as e:
                        logging.warn(f"Error downloading video: {e}")
                        await ctx.send(
                            "There was an error downloading your video, sorry.")
                        return
                    state.playlist.append(video)
                    message = await ctx.send("Added to queue.", embed=video.get_embed())
                else:
                    channel = ctx.author.voice.channel
                    client = ctx.guild.voice_client
                    try:
                        video = Deezerfy(url, ctx.author)
                    except youtube_dl.DownloadError as e:
                        await ctx.send(
                            "There was an error downloading your song, sorry.")
                        return
                    self._play_song_deez(client, state, video, msg)
                    message = await ctx.send("**Now playing:**", embed=video.get_embed())
                    logging.info(f"Now playing '{video.title}'")
            else:
                if client.is_playing():
                    if url.__contains__("open.spotify.com"):
                        url = await spotify(self, ctx, url)
                    try:
                        video = Video(url, ctx.author)
                    except youtube_dl.DownloadError as e:
                        logging.warn(f"Error downloading video: {e}")
                        await ctx.send(
                            "There was an error downloading your video, sorry.")
                        return
                    state.playlist.append(video)
                    message = await ctx.send("Added to queue.", embed=video.get_embed())
                else:
                    if url.__contains__("open.spotify.com"):
                        url = await spotify(self, ctx, url)
                    channel = ctx.author.voice.channel
                    client = ctx.guild.voice_client
                    try:
                        video = Video(url, ctx.author)
                    except youtube_dl.DownloadError as e:
                        await ctx.send(
                            "There was an error downloading your video, sorry.")
                        return
                    self._play_song(client, state, video, msg)
                    message = await ctx.send("**Now playing:**", embed=video.get_embed())
                    logging.info(f"Now playing '{video.title}'")
                
        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                if url.endswith("on deezer") or url.__contains__("https://www.deezer.com/en/track/"):
                    if url.endswith("on deezer"):
                        url = url[:-9] #splices off "on deezer"
                    if url.__contains__("https://www.deezer.com/en/track/"):
                        url = url[32:]
                        url = url.split("?", 1)[0]
                    try:
                        video=Deezerfy(url, ctx.author)
                    except youtube_dl.DownloadError as e: 
                        await ctx.send("Deezer Error, RIP")
                        return
                    client = await channel.connect()
                    self._play_song_deez(client, state, video, msg)
                    message = await ctx.send("**Now playing:**", embed=video.get_embed())
                else:
                    if url.__contains__("open.spotify.com"):
                        url = await spotify(self, ctx, url)
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
                raise commands.CommandError("You're not in a vc dumbass")

    @commands.command()
    @commands.guild_only()
    async def test(self, ctx):
        state = self.get_state(ctx.guild)
        client = ctx.guild.voice_client
        await ctx.send(f'{timeFormat()} / {timeFormat(state.now_playing.get_duration())}')

class GuildState:
    """Helper class managing per-guild state."""

    def __init__(self):
        self.volume = 1.0
        self.playlist = []
        self.now_playing = None

    def is_requester(self, user):
        return self.now_playing.requested_by == user