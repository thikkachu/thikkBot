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

    @commands.command() #clears messages from channel
    async def clear(self, ctx, amount = "10"):
        if (str(ctx.author.id) == '198285838247919616') or (str(ctx.author.id) == '334245365148549120'):
            if amount.lower() == "all":
                await ctx.channel.purge(limit = 101)
            elif amount == "all.OverrideLimit":
                await ctx.channel.purge(limit = 32000000)
            else:
                await ctx.channel.purge(limit = (int(amount) + 1))
        else:
            await ctx.channel.send('You need **MY** permission to use this command **BITCH**.')

#------------------------------/COMMANDS AREA------------------------------#

def setup(thikka): #integrates cog into main.py
    thikka.add_cog(serverManagement(thikka))