import discord
import sys
import traceback
import logging
from discord.ext import commands


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.bot.add_listener(self.on_command_error, "on_command_error")

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return  # Don't interfere with custom error handlers

        error = getattr(error, "original", error)  # get original error

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(
                f"There's no command named that headass. ^help for help (it's in the name tinybrain)"
            )

        if isinstance(error, commands.CommandError):
            return await ctx.send(
                f"`{ctx.command.name}`: {str(error)}")

        await ctx.send(
            "I don't know how you did it, but you fucked up cause I can't process this shit.")
        logging.warn("Ignoring exception in command {}:".format(ctx.command))
        logging.warn("\n" + "".join(
            traceback.format_exception(
                type(error), error, error.__traceback__)))
