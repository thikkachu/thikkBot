import discord
import logging
import sys
from discord.ext import commands
from .cogs import music, error, meta, tips, fun, gambling, serverManagement
from . import config

cfg = config.load_config()

bot = commands.Bot(command_prefix=cfg["prefix"])

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="my life go down the drain '^help'"))

COGS = [music.Music, error.CommandErrorHandler, meta.Meta, tips.Tips, gambling.Gambling, fun.fun, serverManagement.serverManagement]


def add_cogs(bot):
    for cog in COGS:
        bot.add_cog(cog(bot, cfg))  # Initialize the cog and add it to the bot


def run():
    add_cogs(bot)
    if cfg["token"] == "":
        raise ValueError(
            "No token has been provided. Please ensure that config.toml contains the bot token."
        )
        sys.exit(1)
    bot.run(cfg["token"])