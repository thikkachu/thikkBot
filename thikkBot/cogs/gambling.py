#gambling func cog

import discord
from discord.ext import commands
import random
import math
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

    @commands.command(aliases = ['dice', 'die'], brief='^roll <# of sides> <# of times> (Rolls a 6 sided die once by default.)') #returns dice roll(s)
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
        
    
    
    @commands.command(aliases = ['droll'], brief='same as ^roll but in dnd syntax. ^rolld <times>d<sides>') #returns dice roll(s). takes input in dnd syntax.
    async def rolld(self, ctx,*, die = "d6"):
        sender = str(ctx.author)
        senderSpliced = sender[:-5]
        die = die.lower()
        sum = 0
        if die.__contains__("+"):
            
            die = die.split("+")
            rolls = []
            for roll in die:
                if roll.startswith("d"):
                    sides = int(roll.replace('d',''))
                    rolls.append("d"+str(sides) + ": " +str(random.randint(1, int(sides))))
                    sum = sum + random.randint(1, sides)

                elif "d" in roll:
                    roll = roll.strip()
                    times, sides = roll.split('d')
                    for _ in range(int(times)):
                        currentroll = str(random.randint(1, int(sides)))
                        rolls.append("d"+str(sides) + ": " + str(currentroll))
                        sum = sum + int(currentroll)
                    
                else:
                    roll = int(roll)
                    sum = sum + roll
            await ctx.send(f'**{senderSpliced}** rolled **`{rolls}`**.\t Sum: **`[{sum}]`**')
            
                
        else:
            if die.startswith('d'):
                if isinstance(int(die.replace('d','')), commands.BadArgument):
                    await ctx.send("I don't know how you did it, but you fucked up cause I can't process this shit.")
                    return
                sides = int(die.replace('d',''))
                exceedinglyRareThreshold = int(sides*10*math.log(sides))
                exceedinglyRare = random.randint(1,exceedinglyRareThreshold)
                if exceedinglyRare == 1:
                    await ctx.send(f"**{senderSpliced}** rolled `['{sides + 1}']`... What the fuck <:whoah:824444197372166144>?? `(1/{str(exceedinglyRareThreshold)} chance)`")
                else:
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
                    sides = int(sides)
                    exceedinglyRareThreshold = int(sides*10*math.log(sides))
                    exceedinglyRare = random.randint(1,exceedinglyRareThreshold)
                    if exceedinglyRare == 1:
                        await ctx.send(f"**{senderSpliced}** rolled `['{str(sides + 1)}']`... What the fuck <:whoah:824444197372166144>?? `(1/{str(exceedinglyRareThreshold)} chance)`")
                    else:
                        await ctx.send(f'**{senderSpliced}** rolled **`{rolls}`**')
                else:
                    await ctx.send('you did it wrong stupid')


    @commands.command(aliases = ['coinflip', 'flip'], brief = 'Flips a coin. ^flip <# of times> (flips once by default)') #returns a coinflip
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
