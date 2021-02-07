import discord
from discord.ext import commands

import os


bot = commands.Bot(command_prefix="$")


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if str(payload.emoji) == "📇":
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        print(message.content)
    else:
        print("Not match")


@bot.event
async def on_ready():
    bot.load_extension("status")

    bot.remove_command("help")
    bot.load_extension("quotes")
    print(f"Bot ready! Logged in as {bot.user.name} - ID: {bot.user.id}")

bot.run(os.environ["BOT_TOKEN"])
