import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random

responses = ["https://cdn.discordapp.com/attachments/422281194546266126/833994578717442078/unknown.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995657505013800/-tH7mTxLxn7OwnRwmLN3rzGa1ZrYFH2h14HDKZRnpRAUyOOrQj3SAw0GDJEsl_-a06Wo70_lbf61onGw5E_ppDKQ-S2p_6pEB-42.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995680988397568/D3jvOasuTLajHHgMnnmT3k1DPqlDn_N7levmD3rgCXCbtHrkwRF2ZmTrEtx5klRBZva9XUPjXApWlk9iIhjcLuHBLkrd-SAu58Hg.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995738366869504/fpj7zr2bY8-Lxj1R40t7WgHDWeu_0wx4QO3vx1cEXbKHLmJ9U4eaujP4bIcSAAXlDn0wFIGhzkqDfU5cxLctv8V0v1B4uvOoZQ5t.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995793320771604/nzz52_Wx74xXpbdr9xg0az1WTjMjhozCNTnXG98RtgCvkABSIcne37VAqFgM16E6lQQ_UEN4GsHS4-I1u42TzQe_9xKbXmBN7-ac.png", "https://cdn.discordapp.com/attachments/422281194546266126/833995815839203348/FC5uSeyusZAOVnZYXEGn6KMwqxg7VIduFvglVd5lqWPQ0dHF0nYP1r3LNDsbVZP6DO67QIaSzUgID0m40pn6wAx0PH4kypqp4XFB.png", "https://cdn.discordapp.com/attachments/422281194546266126/833998440383512586/BIIjabRf68KJMMCy4RMB6UlpgobR5gH8T9vfx3-bZl8Ix68c4S6nnlbIb2UPKuM3x4Wvsq8lqa5UFPWXY63KIV_7arDDM2_-_uAE.png", "https://cdn.discordapp.com/attachments/422281194546266126/833998708600733696/I1IP-kHqHNpiJjpDyrwb1HFcWAHNUAmKWkuHRLG5brXndQKX_30Dpl5B1OsZp70tI9P9rLF7ZoIc0qc8j8nkSoFiR2AHatIRf1gE.png", "https://cdn.discordapp.com/attachments/422281194546266126/833998952835055616/xOrsM9nWZpjttPaiyL8xhd9oPLLWWaCLKiH8udGEpFTHAZR_xu0dhKY5TgJayHsetTAaRFZy-G6RtKjeYzqTggqvB9SWs5QRpe2n.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999118028111872/2ZxRWZcpieCqMYaocuqjwCnis4VQxu1rhhhNKr0o3hlgr4fIBEjrU1cj3EnHiv_qQAO0upflkEVUxzq-5j5HCgaHZz_nd9uFv937.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999231630180382/unknown.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999352598102096/RO5fWRp0EYZeMpsi3xcF3x8aPDenrsqalE6Feh9CcUEJC1eqyr3B3xK2G2_3A_8TP0q-B8brkIEYTbs93GOrVpaCqIayX7JYkoTO.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999482001293382/af636tf4WGQz630ccxjGxqeHJ4HKnTXmiTZqHz2qhUvFYS9tNi3sj59doPwPlSB6VwviWgouREaWdHYonawMWekuPgcZG1t5HK_G.png", "https://cdn.discordapp.com/attachments/422281194546266126/833999561344286760/DrvdgSwDLL3Rat6LDBRfvDAZP1AijBbsBaL7gSAXjr8n2bq5slOHyK8dkTMUzZwm9EfYK4bebbsbGklujjtPut8kxQ0-BXFMpQPt.png","https://cdn.discordapp.com/attachments/422281194546266126/833999706908655616/t7z7FwPou3ZOjJgrmYDDY8X7a8hcx79gNOSApTqssE2kzYsquCclrsasorUJlJz_vnBgYbf6rc6dqK21nMwxtm6lULMOV7_sDGhX.png","https://cdn.discordapp.com/attachments/422281194546266126/833999815037681685/F9lrYi5BEXqra_bqjTYBbMl7o6zsaFmg8TrgDhkdFyW3nRZPaCgZloGpePEJaWZW4YmT9q6uHo_tlAlTvrdWL7QI3azs-r1IhZLn.png", "https://cdn.discordapp.com/attachments/422281194546266126/834002491606827038/WWcwkZVPqiROAcLc6HFpLOa618UxdA2XBCYwxsyi4eMN3D-GGHWNzYS2XwkizMm6mVy-wKtuokzN83ryi4PrOJEddFzlPNsILK5n.png", "https://cdn.discordapp.com/attachments/422281194546266126/834002799154298900/kc9u96tRM5Ty8qS8nelbqYpQ0jCL1GmGunOJnJXb-E_Eyu_W0V_8ikx1NHY_ZHrgo0Cq_KLaQPMLggEkaJnN3KvnavU35d4JHQrg.png", "https://cdn.discordapp.com/attachments/422281194546266126/834002977404354600/lHKk-5R88yVIpOTihfOFE2lYD8uD2HDsSby3UpZx4Pi7IT1JGiNFEJ5PVvFBdYlFg0dVaBGOqjjOsFxnjXvImvqtyioY4_V9lXGg.png", "https://cdn.discordapp.com/attachments/422281194546266126/834003047550156830/AF1QipPgElK5LklbvvSDoY_MIKdYd5LriH8mfKCVAPK1w698-h393-no.png", "https://cdn.discordapp.com/attachments/422281194546266126/834003181079101440/KcMPGFHEtbj8lhn-8RvpL3TMtcRgpNcfK1EPO64-vKJD0WtbfmXHJmp0-ib08EBvqbj8VJEvkidoholIpTJEYrHg5vWToETw-Xq9.png"]

#-------------------------SHARED METHODS-----------------------------#
def unspace(str):
    str = str.replace(' ', '')
    return str

def unspaceList(arr):
    for i in range(len(arr)):
        arr[i-1] = unspace(arr[i-1])
    return arr

#-------------------------/SHARED METHODS-----------------------------#

#-------------------------INITIALIZES COG ENV-----------------------------#
class math(commands.Cog):
    #cog init
    def __init__ (self, bot, config):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('MATH Cog loaded successfully.')

#-------------------------INITIALIZES COG ENV-----------------------------#

#------------------------------COMMANDS AREA------------------------------#
    
    @commands.command(aliases=['sum','plus','addition', '+'])
    async def add(self, ctx, *, addends = 'placeholder'): #simple addition
        
        if addends == 'placeholder':
            await ctx.send('You gave no numbers for me to add so uhhhh... 1+1 = 2 <:Yesss:721804195539320895>')
        
        elif addends.__contains__('+'):
            addends = list(map(int, unspaceList(addends.split('+'))))
            
            await ctx.send(f'Sum: `{str(sum(addends))}`')

        else:
            addends = list(map(int, unspaceList(addends.split())))
            await ctx.send(f'Sum: `{str(sum(addends))}`')

    @commands.command(aliases=['minus', '-', 'difference', 'subtraction'])
    async def subtract(self, ctx, minuend = 'placeholder', *, subtrahends = 'placeholder'): #simple subtraction
        sender = str(ctx.author)
        senderSpliced = sender[:-5]
        if minuend == 'placeholder':
            await ctx.send(f"Bruh... {senderSpliced} goes and tells me to go and subtract shit when there's nothing to subtract. \n `Syntax: ^subtract <minuend> <subtrahends>`")
        
        elif minuend.__contains__('-') and (subtrahends == 'placeholder'):
            minuend, subtrahends = minuend.split("-", 1)
            minuend = int(unspace(minuend.replace('-', '')))
            subtrahends = list(map(int, unspaceList(subtrahends.split('-'))))
            subtrahend = sum(subtrahends)
            await ctx.send(f'Difference: `{str(minuend - subtrahend)}`')

        elif minuend.__contains__('-') or subtrahends.__contains__('-'):
            minuend = int(unspace(minuend.replace('-', '')))
            subtrahends = list(map(int, unspaceList(subtrahends.split('-'))))
            subtrahend = sum(subtrahends)
            await ctx.send(f'Difference: `{str(minuend - subtrahend)}`')

        else:
            subtrahends = list(map(int, unspaceList(subtrahends.split())))
            subtrahend = sum(subtrahends)
            await ctx.send(f'Difference: `{str(int(minuend) - subtrahend)}`')
#------------------------------/COMMANDS AREA------------------------------#

def setup(bot): #integrates cog into main.py
    bot.add_cog(math(bot))