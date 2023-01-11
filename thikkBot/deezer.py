from pydeezer import Deezer
import discord
import os
import glob

arl =  ""
deezer = Deezer(arl=arl)
user_info = deezer.user

from pydeezer import Downloader
from pydeezer.constants import track_formats

downloadDir = '/Users/fermioni/Code/Thikkbot/thikkBot/cogs/tempMusic' #set this manually and arl

class Deezerfy:

    def __init__(self, search, requested_by):
        if search.isdigit():
            song = deezer.get_track(search)['info']
            data = song['DATA']
            list_ids = [search]
            downloader = Downloader(deezer, list_ids, downloadDir, quality=track_formats.MP3_320, concurrent_downloads=1)
            downloader.start()
            os.chdir("/Users/fermioni/Code/Thikkbot/thikkBot/cogs/tempMusic") #set manually #########################
            for file in glob.glob(data["SNG_TITLE"] + "*.mp3"):
                os.rename(file, data['SNG_TITLE'] + ".mp3")
            for file in glob.glob(data["SNG_TITLE"] + "*.lrc"):
                os.rename(file, data['SNG_TITLE'] + ".lrc")
            self.title = data['SNG_TITLE']
            self.stream_url_128 = deezer.get_track_download_url(song, "MP3_128")[0]
            self.stream_url_256 = deezer.get_track_download_url(song, "MP3_256")[0]
            self.stream_url_320 = deezer.get_track_download_url(song, "MP3_320")[0]
            self.stream_url_flac =deezer.get_track_download_url(song, "FLAC")[0]
            self.page_link = "https://www.deezer.com/en/track/" + search
            self.title = data["SNG_TITLE"]
            self.artist = data['ART_NAME']
            self.thumbnail = "https://api.deezer.com/album/"+ data["ALB_ID"] + "/image'"
            self.requested_by = requested_by
            self.duration = data['DURATION']
    
        else:
            song = deezer.search_tracks(search)
            song = song[0]
            list_ids = [song['id']]
            downloader = Downloader(deezer, list_ids, downloadDir, quality=track_formats.MP3_320, concurrent_downloads=1)
            downloader.start()
            os.chdir("/Users/fermioni/Code/Thikkbot/thikkBot/cogs/tempMusic") #set manually #########################
            for file in glob.glob(song["title"] + "*.mp3"):
                os.rename(file, song['title'] + ".mp3")
            for file in glob.glob(song["title"] + "*.lrc"):
                os.rename(file, song['title'] + ".lrc")
            self.title = song['title']
            self.stream_url_128 = deezer.get_track_download_url(deezer.get_track(song['id'])['info'], "MP3_128")[0]
            self.stream_url_256 = deezer.get_track_download_url(deezer.get_track(song['id'])['info'], "MP3_256")[0]
            self.stream_url_320 = deezer.get_track_download_url(deezer.get_track(song['id'])['info'], "MP3_320")[0]
            self.stream_url_flac =deezer.get_track_download_url(deezer.get_track(song['id'])['info'], "FLAC")[0]
            self.page_link = song["link"]
            self.title = song["title"]
            self.artist = song['artist']['name']
            self.thumbnail = song['album']['cover']
            self.requested_by = requested_by
            self.duration = song['duration']
    
    def get_embed(self):
        """Makes an embed out of this Video's information."""
        embed = discord.Embed(
            title=self.title, description=self.artist,  url=self.page_link)
        embed.set_footer(
            text=f"Requested by {self.requested_by.name}",
            icon_url=self.requested_by.avatar)
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        return embed
    def embed128(self):
        embed = discord.Embed(title="MP3-128", description="Low Quality",  url=self.stream_url_128)
        return embed
    def embed256(self):
        embed = discord.Embed(title="MP3-256", description="Mid Quality",  url=self.stream_url_256)
        return embed
    def embed320(self):
        embed = discord.Embed(title="MP3-320", description="High Quality (Compressed)",  url=self.stream_url_320)
        return embed
    def embedflac(self):
        embed = discord.Embed(title="FLAC", description="High Quality (Lossless)",  url=self.stream_url_flac)
        return embed




    def get_duration(self):
        return self.duration

    