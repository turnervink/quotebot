import discord
from discord.ext import bridge

import os

import db
import util


intents = discord.Intents.default()
bot = bridge.Bot(debug_guilds=["339533012725268480"], command_prefix="$", intents=intents)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if str(payload.emoji) == "📇":
        channel = bot.get_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)
        author = db.get_author(message.author)
        message_date_str = util.get_quote_date(message)

        if author is None:
            author = message.author.name

        db.add_quote(str(message.id), message.content, author, message_date_str)
        await channel.send(f"{payload.member.mention} Quote added!")


@bot.event
async def on_ready():
    bot.load_extension("backup")
    bot.load_extension("status")

    bot.remove_command("help")
    bot.load_extension("quotes")
    print(f"Bot ready! Logged in as {bot.user.name} - ID: {bot.user.id}")

bot.run(os.environ["BOT_TOKEN"])
