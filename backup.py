from discord.ext import commands

import db

from datetime import datetime
import json
import os


def do_backup(data):
    now = datetime.now()
    db_root = os.environ["DB_ROOT"]
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S")
    with open(f"{os.environ['BACKUP_DIR']}/{db_root} {timestamp}.json", "w") as outfile:
        json.dump(data, outfile)


class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="backup")
    async def backup_quotes(self, ctx):
        quotes = db.get_quotes()
        do_backup(quotes)
        await ctx.send(f"{ctx.message.author.mention} Backup created!")


def setup(bot: commands.Bot):
    bot.add_cog(Backup(bot))
