import os

import discord
from discord.ext import commands, tasks

import db


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.postgres = db.Postgres(
            os.environ["POSTGRES_HOST"],
            os.environ["POSTGRES_PORT"],
            os.environ["POSTGRES_DATABASE"],
            os.environ["POSTGRES_USERNAME"],
            os.environ["POSTGRES_PASSWORD"]
        )
        self.update_status.start()

    @tasks.loop(hours=6)
    async def update_status(self):
        random_quote = self.postgres.get_random_quote()

        if random_quote is not None:
            text = random_quote["quote"]
            author = random_quote["author"]
            await self.bot.change_presence(activity=discord.Game(name=f"\"{text}\" - {author}"))

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
