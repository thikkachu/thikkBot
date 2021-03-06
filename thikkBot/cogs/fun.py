import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random

responses = ["https://cdn.discordapp.com/attachments/422281194546266126/833994578717442078/unknown.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995657505013800/-tH7mTxLxn7OwnRwmLN3rzGa1ZrYFH2h14HDKZRnpRAUyOOrQj3SAw0GDJEsl_-a06Wo70_lbf61onGw5E_ppDKQ-S2p_6pEB-42.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995680988397568/D3jvOasuTLajHHgMnnmT3k1DPqlDn_N7levmD3rgCXCbtHrkwRF2ZmTrEtx5klRBZva9XUPjXApWlk9iIhjcLuHBLkrd-SAu58Hg.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995738366869504/fpj7zr2bY8-Lxj1R40t7WgHDWeu_0wx4QO3vx1cEXbKHLmJ9U4eaujP4bIcSAAXlDn0wFIGhzkqDfU5cxLctv8V0v1B4uvOoZQ5t.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995793320771604/nzz52_Wx74xXpbdr9xg0az1WTjMjhozCNTnXG98RtgCvkABSIcne37VAqFgM16E6lQQ_UEN4GsHS4-I1u42TzQe_9xKbXmBN7-ac.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995815839203348/FC5uSeyusZAOVnZYXEGn6KMwqxg7VIduFvglVd5lqWPQ0dHF0nYP1r3LNDsbVZP6DO67QIaSzUgID0m40pn6wAx0PH4kypqp4XFB.png", "https://cdn.discordapp.com/attachments/422281194546266126/833998440383512586/BIIjabRf68KJMMCy4RMB6UlpgobR5gH8T9vfx3-bZl8Ix68c4S6nnlbIb2UPKuM3x4Wvsq8lqa5UFPWXY63KIV_7arDDM2_-_uAE.png", "https://cdn.discordapp.com/attachments/422281194546266126/833998708600733696/I1IP-kHqHNpiJjpDyrwb1HFcWAHNUAmKWkuHRLG5brXndQKX_30Dpl5B1OsZp70tI9P9rLF7ZoIc0qc8j8nkSoFiR2AHatIRf1gE.png", "https://cdn.discordapp.com/attachments/422281194546266126/833998952835055616/xOrsM9nWZpjttPaiyL8xhd9oPLLWWaCLKiH8udGEpFTHAZR_xu0dhKY5TgJayHsetTAaRFZy-G6RtKjeYzqTggqvB9SWs5QRpe2n.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999118028111872/2ZxRWZcpieCqMYaocuqjwCnis4VQxu1rhhhNKr0o3hlgr4fIBEjrU1cj3EnHiv_qQAO0upflkEVUxzq-5j5HCgaHZz_nd9uFv937.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999231630180382/unknown.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999352598102096/RO5fWRp0EYZeMpsi3xcF3x8aPDenrsqalE6Feh9CcUEJC1eqyr3B3xK2G2_3A_8TP0q-B8brkIEYTbs93GOrVpaCqIayX7JYkoTO.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999482001293382/af636tf4WGQz630ccxjGxqeHJ4HKnTXmiTZqHz2qhUvFYS9tNi3sj59doPwPlSB6VwviWgouREaWdHYonawMWekuPgcZG1t5HK_G.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999561344286760/DrvdgSwDLL3Rat6LDBRfvDAZP1AijBbsBaL7gSAXjr8n2bq5slOHyK8dkTMUzZwm9EfYK4bebbsbGklujjtPut8kxQ0-BXFMpQPt.png","https://cdn.discordapp.com/attachments/422281194546266126/833999706908655616/t7z7FwPou3ZOjJgrmYDDY8X7a8hcx79gNOSApTqssE2kzYsquCclrsasorUJlJz_vnBgYbf6rc6dqK21nMwxtm6lULMOV7_sDGhX.png","https://cdn.discordapp.com/attachments/422281194546266126/833999815037681685/F9lrYi5BEXqra_bqjTYBbMl7o6zsaFmg8TrgDhkdFyW3nRZPaCgZloGpePEJaWZW4YmT9q6uHo_tlAlTvrdWL7QI3azs-r1IhZLn.png", "https://cdn.discordapp.com/attachments/422281194546266126/834002491606827038/WWcwkZVPqiROAcLc6HFpLOa618UxdA2XBCYwxsyi4eMN3D-GGHWNzYS2XwkizMm6mVy-wKtuokzN83ryi4PrOJEddFzlPNsILK5n.png", "https://cdn.discordapp.com/attachments/422281194546266126/834002799154298900/kc9u96tRM5Ty8qS8nelbqYpQ0jCL1GmGunOJnJXb-E_Eyu_W0V_8ikx1NHY_ZHrgo0Cq_KLaQPMLggEkaJnN3KvnavU35d4JHQrg.png", "https://cdn.discordapp.com/attachments/422281194546266126/834002977404354600/lHKk-5R88yVIpOTihfOFE2lYD8uD2HDsSby3UpZx4Pi7IT1JGiNFEJ5PVvFBdYlFg0dVaBGOqjjOsFxnjXvImvqtyioY4_V9lXGg.png", "https://cdn.discordapp.com/attachments/422281194546266126/834003047550156830/AF1QipPgElK5LklbvvSDoY_MIKdYd5LriH8mfKCVAPK1w698-h393-no.png", "https://cdn.discordapp.com/attachments/422281194546266126/834003181079101440/KcMPGFHEtbj8lhn-8RvpL3TMtcRgpNcfK1EPO64-vKJD0WtbfmXHJmp0-ib08EBvqbj8VJEvkidoholIpTJEYrHg5vWToETw-Xq9.png"]

#-------------------------INITIALIZES COG ENV-----------------------------#

class fun(commands.Cog):
    #cog init
    def __init__ (self, bot, config):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('FUN Cog loaded successfully.')

#-------------------------INITIALIZES COG ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------#

    @commands.command()   #returns a friendly message to the user
    @commands.guild_only()
    async def thikk(self, ctx, *, misc = ""):
        sender = str(ctx.author)
        senderSpliced = sender[:-5]
        senderID = str(ctx.author.id)
        if (senderID == "194755723719213056") or (senderID == '393246131049463818'): #aaronjane
            await ctx.send("I regret to inform you that you are, indeed, a **faggot!**")
        elif senderID == "334245365148549120": #me
            await ctx.send("Hello **Master!!** UwU OwO 88w88 :3")
        elif (senderID == '311321262745976843') or (senderID == '422176005772541963'):
            await ctx.send("https://cdn.discordapp.com/attachments/422281194546266126/836378504974565396/download_1.jpg")
        elif (senderID == '799811805748658196') or (senderID == '347599940169760788'):
            await ctx.send("Jacob I don't know why you're so superficially mean to me. I apologize for any past transgressions I may have incurred and am hoping your future life and family are enjoyable. :)")
        elif senderID == '198285838247919616': #robert
            await ctx.send("Hello there **protag-sama~~~**. :heart_eyes:")
        elif senderID == '219923344429023234': #ezan
            await ctx.send("You're grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded, grounded. You hate to see it :cry:")
        elif senderID == '314236066167128085': #jonag
            await ctx.send(":eggplant:Well you see the thing is**-**")
        elif senderID == '387829620197687308': #partake
            await ctx.send("Hello scav! I hope Jonah's dick entered your mouth at one point! :drool:")
        elif senderID == '198327607312252929': #inan
            await ctx.send(":musical_note::musical_note::musical_note::bird::tv:")
        elif senderID == '831802831018524672': #feedback error.jpig
            await ctx.send("AYO WHAT THE FUCK! THIS AINT POSSIBLE. NAH NAH NAH NAH NO NO NO FUCK OFF. :angryflushed:")
        
        else:
            await ctx.send(f"fuck you **{senderSpliced}**")
    
    @commands.command(brief = "Roll a random picture of thikk's cat. (there's 2 exceedingly rare occurrences)")   #returns a random cat picture (pulls from speech.json)
    async def cat(self, ctx):
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

    @commands.command(aliases = ['sex?'], brief = "Decides whether or not sex.")    #sex
    async def sex(self,ctx, *, misc = ""):
        gifs = ['https://tenor.com/view/ena-ena-extinction-party-yes-auction-day-ena-auction-day-gif-19851364', 'https://tenor.com/view/ena-ena-joel-g-joel-g-ena-ena-extinction-party-extinction-party-ena-gif-18960646']
        choice = random.choice(gifs)
        if choice == gifs[0]:
            await ctx.send(f'{choice}')
            await ctx.send("Yes **SEX** :flushed:")
        elif choice == gifs[1]:
            await ctx.send(f'{choice}')
            await ctx.send("NO. **NO SEX** :angry:")

    # @commands.command()
    # async def eat(self, ctx, *, misc = ''):
    #     misc = misc.lower()
    #     if misc.__contains__("shit"):
    #         await ctx.send("That would be quite unsanitary. Also stay away from scat you kinky bitch.")
    #     elif misc.__contains__("cock"):
    #         await ctx.send("Sorry cunt, im lesbian.", file=licc)
#------------------------------/COMMANDS AREA------------------------------#

def setup(bot): #integrates cog into main.py
    bot.add_cog(fun(bot))