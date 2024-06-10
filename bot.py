import json
import os

import util

import discord
from discord.ext import commands

intents = discord.Intents()

try:
    debug_guild_ids = json.loads(os.environ['DEBUG_GUILD_IDS'])
    print("Starting bot with debug_guilds=" + str(debug_guild_ids))
    bot = discord.Bot(intents=intents, debug_guilds=debug_guild_ids)
except KeyError:
    print("No debug_guilds specified, will create global commands")
    bot = discord.Bot(intents=intents)


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"You're doing that too much! Try again in {util.humanize_cooldown(error.retry_after)}.")


@bot.event
async def on_ready():
    print(f"Bot ready! Logged in as {bot.user.name} - ID: {bot.user.id}")

bot.load_extension("status")
bot.load_extension("quotes")
bot.run(os.environ["BOT_TOKEN"])
