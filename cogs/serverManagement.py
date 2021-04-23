#server management commands cog

import discord
from discord.ext import commands
import random

#-------------------------INITIALIZES COG ENV-----------------------------#

class serverManagement(commands.Cog):
    #cog init
    def __init__ (self, thikka):
        self.thikka = thikka 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Server Management Cog loaded successfully.')

#-------------------------/INITIALIZES COG ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------#

    @commands.command() #returns bot latency to the user
    async def ping(self, ctx):
        await ctx.send(str(f'I have a ping of **{round(self.thikka.latency*1000)}**ms.'))

    @commands.command() #clears messages from channel'
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount = "10"):
        if amount.lower() == "all":
            await ctx.channel.purge(limit = 101)
        elif amount == "all.OverrideLimit":
            await ctx.channel.purge(limit = 32000000)
        else:
            await ctx.channel.purge(limit = (int(amount) + 1))

#------------------------------/COMMANDS AREA------------------------------#

def setup(thikka): #integrates cog into main.py
    thikka.add_cog(serverManagement(thikka))