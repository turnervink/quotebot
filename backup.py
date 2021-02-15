from discord.ext import commands, tasks

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
        self.scheduled_backup.start()

    @commands.command(name="backup")
    async def backup_quotes(self, ctx):
        quotes = db.get_quotes()
        do_backup(quotes)
        await ctx.send(f"{ctx.message.author.mention} Backup created!")

    @tasks.loop(hours=24)
    async def scheduled_backup(self):
        print("Running scheduled quote backup...")
        quotes = db.get_quotes()
        do_backup(quotes)
        print("Backup successful!")

    @scheduled_backup.before_loop
    async def before_scheduled_backup(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(Backup(bot))
