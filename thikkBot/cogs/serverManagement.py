#server management commands cog

import discord
from discord.ext import commands
import random

#-------------------------INITIALIZES COG ENV-----------------------------#

class serverManagement(commands.Cog):
    #cog init
    def __init__ (self, bot, config):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Server Management Cog loaded successfully.')

#-------------------------/INITIALIZES COG ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------#

    @commands.command(brief = 'Returns bot latency') #returns bot latency to the user
    async def ping(self, ctx):
        await ctx.send(str(f'I have a ping of **{round(self.bot.latency*1000)}**ms.'))

    @commands.command(brief = '^clear <# of messages to delete> (defaults to 10 messages. all to delete 100. all.OverrideLimit to delete entire channel)') #clears messages from channel'
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount = "10"):
        if amount.lower() == "all":
            await ctx.channel.purge(limit = 101)
        elif amount == "all.OverrideLimit":
            await ctx.channel.purge(limit = 32000000)
        else:
            await ctx.channel.purge(limit = (int(amount) + 1))

    #---------cog management area--------#

    @commands.command(brief = "thikk's use only") #loads cog file
    async def load(self, ctx, ext = "placeholder"):
        if ext == "placeholder":
            await ctx.send("Syntax: `^load (cog name)`")
        if (str(ctx.author.id) == "334245365148549120") or (str(ctx.author.id) == '198285838247919616'): 
            self.bot.load_extension(f'cogs.{ext}')
            await ctx.send(f'`{ext}` loaded successfully')
            print(f'`{ext}` cog loaded successfully')
        else:
            await ctx.send('fuck off cunt')
    @commands.command(brief = "thikk's use only") #unloads cog file
    async def unload(self, ctx, ext = "placeholder"):
        if ext == "placeholder":
            await ctx.send("Syntax: `^unload (cog name)`")
        elif (str(ctx.author.id) == "334245365148549120") or (str(ctx.author.id) == '198285838247919616'): 
            self.bot.unload_extension(f'cogs.{ext}')
            await ctx.send(f'`{ext}` unloaded successfully')
            print(f'`{ext}` cog unloaded successfully')
        else:
            await ctx.send('fuck off cunt')
    @commands.command(brief = "thikk's use only") #reloads cog file
    async def reload(self, ctx, ext = "placeholder"):
        if ext == "placeholder":
            await ctx.send("Syntax: `^reload (cog name)`")
        elif (str(ctx.author.id) == "334245365148549120") or (str(ctx.author.id) == '198285838247919616'):       
            self.bot.unload_extension(f'cogs.{ext}')
            self.bot.load_extension(f'cogs.{ext}')
            await ctx.send(f'`{ext}` reloaded successfully')
            print(f'`{ext}` cog reloaded successfully')
        else:
            await ctx.send('fuck off cunt')

#---------/cog management area--------#

#------------------------------/COMMANDS AREA------------------------------#

def setup(bot): #integrates cog into main.py
    bot.add_cog(serverManagement(bot))