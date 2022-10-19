import json
import os

import discord

import db
import util

intents = discord.Intents(messages=True, reactions=True, message_content=True)

try:
    debug_guild_ids = json.loads(os.environ['DEBUG_GUILD_IDS'])
    print("Starting bot with debug_guilds=" + str(debug_guild_ids))
    bot = discord.Bot(intents=intents, debug_guilds=debug_guild_ids)
except KeyError:
    print("No debug_guilds specified, will create global commands")
    bot = discord.Bot(intents=intents)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if str(payload.emoji) == "📇":
        channel = await bot.fetch_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)
        author = db.get_author(message.author)
        message_date_str = util.get_quote_date(message)

        if author is None:
            author = message.author.name

        db.add_quote(str(message.id), message.content, author, message_date_str)
        await channel.send(f"{payload.member.mention} Quote added!")


@bot.event
async def on_ready():
    print(f"Bot ready! Logged in as {bot.user.name} - ID: {bot.user.id}")

bot.load_extension("status")
bot.load_extension("quotes")
bot.run(os.environ["BOT_TOKEN"])
