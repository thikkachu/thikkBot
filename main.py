#made by thikkachu.

import discord
from discord.ext import commands
import random
import json

#-------------------------INITIALIZES BOT ENV-----------------------------#

thikka = commands.Bot(command_prefix='^')
with open ("speech.json") as file:
    data = json.load(file)
with open ("key.json") as file:
    key = json.load(file)
@thikka.event
async def on_ready():
    print("{0.user} ready".format(thikka))

#-------------------------/INITIALIZES BOT ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------#

@thikka.command()   #returns bot latency to the user
async def ping(ctx):
    await ctx.send(str(f'I have a ping of **{round(thikka.latency * 1000)}**ms.'))

@thikka.command()   #returns a friendly message to the user
async def thikk(ctx):
    sender = str(ctx.author)
    senderSpliced = sender[:-5]
    senderID = str(ctx.author.id)
    if senderID == "194755723719213056":
        await ctx.send("I regret to inform you that you are, indeed, a **faggot!**")
    if senderID == "334245365148549120":
        await ctx.send("Hello **Master!!** UwU OwO 88w88 :3")
    else:
        await ctx.send(f"fuck you **{senderSpliced}**")

@thikka.command()   #returns a random cat picture (pulls from speech.json)
async def cat(ctx):
    responses = data['responses']
    sender = str(ctx.author)
    senderSpliced = sender[:-5]
    cat = random.choice(responses)
    roll = random.randint(1,404)
    roll2 = random.randint(1,690)
    if roll == 403:
        await ctx.send('https://rb.gy/3z05kj')
        await ctx.send("404 Feline Not Found. As a compensation for this mistake, please take NUT CAT **%s** (1/404 Chance)"%(senderSpliced))
    elif roll2 == 600:
        await ctx.send('https://rb.gy/npvo9w')
        await ctx.send('Xavier')
    else:
        await ctx.send(cat)

@thikka.command()   #returns dice roll [syntax: (^roll {sides} {times})]
async def roll(ctx, sides = 6, times = 1, *, misc = ""):
    sender = str(ctx.author)
    senderSpliced = sender[:-5]
    rolls = []
    for i in range(int(times)):
        rolls.append(str(random.randint(1, int(sides))))
    await ctx.send(f'**{senderSpliced}** rolled **`{rolls}`**')
@roll.error #error handler for roll func
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I don't know how you did it, but you fucked up cause I can't process this shit.")


@thikka.command()   #returns dice roll in dnd syntax [{times}d{sides}]
async def rolld(ctx, die = "d6", *, misc = ""):
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
@rolld.error #error handler for rolld func
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I don't know how you did it, but you fucked up cause I can't process this shit.")


@thikka.command() #clears messages from server
async def clear(ctx, amount = "10"):
    
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


#-------------------------JOIN/LEAVE MESSAGE AREA-------------------------#

@thikka.event
async def on_member_join(member):
    print(f'{member} is here to waste their life')

@thikka.event
async def on_member_remove(member):
    print(f'{member} is gone')

#-------------------------/JOIN/LEAVE MESSAGE AREA-------------------------#

thikka.run(key['key'])