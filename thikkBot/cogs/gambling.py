#gambling func cog

import discord
from discord.ext import commands
import random
coinflip = ["`heads.` Now give some.", "`*tails`... furry lookin ass.*","`head`ededededededs", "Miles Tails Prower (`tails`).", "ooga booga, monkey want `head`.", "tailgating your mom's dump truck (`tails`)."]
#-------------------------INITIALIZES COG ENV-----------------------------#

class Gambling(commands.Cog):
    #cog init
    def __init__ (self, bot, config):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Gambling Cog loaded successfully.')

#-------------------------/INITIALIZES COG ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------#

    @commands.command(aliases = ['dice', 'die']) #returns dice roll(s)
    async def roll(self, ctx, sides = 6, times = 1, *, misc = ''):
        sender = str(ctx.author)
        senderSpliced = sender[:-5]
        rolls = []
        sum = 0
        for i in range(int(times)):
            rolls.append(str(random.randint(1, int(sides))))
        for i in range(len(rolls)):
            sum = sum + int(rolls[i])
        await ctx.send(f'**{senderSpliced}** rolled **`{rolls}`**')  
        
    
    
    @commands.command(aliases = ['droll']) #returns dice roll(s). takes input in dnd syntax.
    async def rolld(self, ctx, die = "d6", *, misc = ""):
        sender = str(ctx.author)
        senderSpliced = sender[:-5]
        die = die.lower()
        if die.startswith('d'):
            if isinstance(int(die.replace('d','')), commands.BadArgument):
                await ctx.send("I don't know how you did it, but you fucked up cause I can't process this shit.")
                return
            sides = int(die.replace('d',''))
            await ctx.send(f"**{senderSpliced}** rolled `['{str(random.randint(1, sides))}']`")

        else:
            times, sides = die.split('d')
            rolls = []
            for i in range(int(times)):
                rolls.append(str(random.randint(1, int(sides))))
            sum = 0
            for i in range(len(rolls)):
                sum = sum + int(rolls[i])
            if int(times) > 1:
                await ctx.send(f'**{senderSpliced}** rolled **`{rolls}`**.\t Sum: **`[{sum}]`**')
            elif int(times) == 1:
                await ctx.send(f'**{senderSpliced}** rolled **`{rolls}`**')
            else:
                await ctx.send('you did it wrong stupid')


    @commands.command(aliases = ['coinflip', 'flip']) #returns a coinflip
    async def coin(self, ctx, amount = 1):
        sender = str(ctx.author)
        senderSpliced = sender[:-5] 
        if amount == 1:
            flip = random.choice(coinflip)
            await ctx.send(f"**{senderSpliced}'s** coin landed on {flip}")
        elif amount > 1:
            flip = []
            for _ in range(amount):
                flip.append(random.choice(['heads','tails']))
            await ctx.send(f"**{senderSpliced}'s** coin flips landed on: `{flip}`")

#------------------------------/COMMANDS AREA------------------------------#

def setup(bot): #integrates cog into main.py
    bot.add_cog(Gambling(bot))