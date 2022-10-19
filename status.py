import discord
from discord.ext import commands, tasks

import random

import db


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quotes = db.get_quotes()
        self.update_status.start()

    @tasks.loop(hours=6)
    async def update_status(self):
        self.quotes = db.get_quotes()

        if self.quotes is not None:
            quote = self.quotes[random.choice(list(self.quotes.keys()))]

            text = quote["quote"]
            author = quote["author"]
            await self.bot.change_presence(activity=discord.Game(name=f"\"{text}\" - {author}"))

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
