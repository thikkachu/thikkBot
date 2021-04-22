import discord
from discord.ext import commands
import random

responses = ["https://cdn.discordapp.com/attachments/422281194546266126/833994578717442078/unknown.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995657505013800/-tH7mTxLxn7OwnRwmLN3rzGa1ZrYFH2h14HDKZRnpRAUyOOrQj3SAw0GDJEsl_-a06Wo70_lbf61onGw5E_ppDKQ-S2p_6pEB-42.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995680988397568/D3jvOasuTLajHHgMnnmT3k1DPqlDn_N7levmD3rgCXCbtHrkwRF2ZmTrEtx5klRBZva9XUPjXApWlk9iIhjcLuHBLkrd-SAu58Hg.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995738366869504/fpj7zr2bY8-Lxj1R40t7WgHDWeu_0wx4QO3vx1cEXbKHLmJ9U4eaujP4bIcSAAXlDn0wFIGhzkqDfU5cxLctv8V0v1B4uvOoZQ5t.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995793320771604/nzz52_Wx74xXpbdr9xg0az1WTjMjhozCNTnXG98RtgCvkABSIcne37VAqFgM16E6lQQ_UEN4GsHS4-I1u42TzQe_9xKbXmBN7-ac.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995815839203348/FC5uSeyusZAOVnZYXEGn6KMwqxg7VIduFvglVd5lqWPQ0dHF0nYP1r3LNDsbVZP6DO67QIaSzUgID0m40pn6wAx0PH4kypqp4XFB.png", "https://cdn.discordapp.com/attachments/422281194546266126/833998440383512586/BIIjabRf68KJMMCy4RMB6UlpgobR5gH8T9vfx3-bZl8Ix68c4S6nnlbIb2UPKuM3x4Wvsq8lqa5UFPWXY63KIV_7arDDM2_-_uAE.png", "https://cdn.discordapp.com/attachments/422281194546266126/833998708600733696/I1IP-kHqHNpiJjpDyrwb1HFcWAHNUAmKWkuHRLG5brXndQKX_30Dpl5B1OsZp70tI9P9rLF7ZoIc0qc8j8nkSoFiR2AHatIRf1gE.png", "https://cdn.discordapp.com/attachments/422281194546266126/833998952835055616/xOrsM9nWZpjttPaiyL8xhd9oPLLWWaCLKiH8udGEpFTHAZR_xu0dhKY5TgJayHsetTAaRFZy-G6RtKjeYzqTggqvB9SWs5QRpe2n.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999118028111872/2ZxRWZcpieCqMYaocuqjwCnis4VQxu1rhhhNKr0o3hlgr4fIBEjrU1cj3EnHiv_qQAO0upflkEVUxzq-5j5HCgaHZz_nd9uFv937.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999231630180382/unknown.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999352598102096/RO5fWRp0EYZeMpsi3xcF3x8aPDenrsqalE6Feh9CcUEJC1eqyr3B3xK2G2_3A_8TP0q-B8brkIEYTbs93GOrVpaCqIayX7JYkoTO.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999482001293382/af636tf4WGQz630ccxjGxqeHJ4HKnTXmiTZqHz2qhUvFYS9tNi3sj59doPwPlSB6VwviWgouREaWdHYonawMWekuPgcZG1t5HK_G.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999561344286760/DrvdgSwDLL3Rat6LDBRfvDAZP1AijBbsBaL7gSAXjr8n2bq5slOHyK8dkTMUzZwm9EfYK4bebbsbGklujjtPut8kxQ0-BXFMpQPt.png","https://cdn.discordapp.com/attachments/422281194546266126/833999706908655616/t7z7FwPou3ZOjJgrmYDDY8X7a8hcx79gNOSApTqssE2kzYsquCclrsasorUJlJz_vnBgYbf6rc6dqK21nMwxtm6lULMOV7_sDGhX.png","https://cdn.discordapp.com/attachments/422281194546266126/833999815037681685/F9lrYi5BEXqra_bqjTYBbMl7o6zsaFmg8TrgDhkdFyW3nRZPaCgZloGpePEJaWZW4YmT9q6uHo_tlAlTvrdWL7QI3azs-r1IhZLn.png", "https://cdn.discordapp.com/attachments/422281194546266126/834002491606827038/WWcwkZVPqiROAcLc6HFpLOa618UxdA2XBCYwxsyi4eMN3D-GGHWNzYS2XwkizMm6mVy-wKtuokzN83ryi4PrOJEddFzlPNsILK5n.png", "https://cdn.discordapp.com/attachments/422281194546266126/834002799154298900/kc9u96tRM5Ty8qS8nelbqYpQ0jCL1GmGunOJnJXb-E_Eyu_W0V_8ikx1NHY_ZHrgo0Cq_KLaQPMLggEkaJnN3KvnavU35d4JHQrg.png", "https://cdn.discordapp.com/attachments/422281194546266126/834002977404354600/lHKk-5R88yVIpOTihfOFE2lYD8uD2HDsSby3UpZx4Pi7IT1JGiNFEJ5PVvFBdYlFg0dVaBGOqjjOsFxnjXvImvqtyioY4_V9lXGg.png", "https://cdn.discordapp.com/attachments/422281194546266126/834003047550156830/AF1QipPgElK5LklbvvSDoY_MIKdYd5LriH8mfKCVAPK1w698-h393-no.png", "https://cdn.discordapp.com/attachments/422281194546266126/834003181079101440/KcMPGFHEtbj8lhn-8RvpL3TMtcRgpNcfK1EPO64-vKJD0WtbfmXHJmp0-ib08EBvqbj8VJEvkidoholIpTJEYrHg5vWToETw-Xq9.png"]
#-------------------------INITIALIZES COG ENV-----------------------------#

class fun(commands.Cog):
    #cog init
    def __init__ (self, thikka):
        self.thikka = thikka 

    @commands.Cog.listener()
    async def on_ready(self):
        print('FUN Cog loaded successfully.')

#-------------------------INITIALIZES COG ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------#

    @commands.command()   #returns a friendly message to the user
    async def thikk(self, ctx, *, misc = ""):
        sender = str(ctx.author)
        senderSpliced = sender[:-5]
        senderID = str(ctx.author.id)
        if senderID == "194755723719213056":
            await ctx.send("I regret to inform you that you are, indeed, a **faggot!**")
        if senderID == "334245365148549120":
            await ctx.send("Hello **Master!!** UwU OwO 88w88 :3")
        else:
            await ctx.send(f"fuck you **{senderSpliced}**")
    
    @commands.command()   #returns a random cat picture (pulls from speech.json)
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

#------------------------------/COMMANDS AREA------------------------------#

def setup(thikka): #integrates cog into main.py
    thikka.add_cog(fun(thikka))