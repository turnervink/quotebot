import discord
from discord.ext import commands

from db import db

import random


class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quotes = db.reference("quotes").get()

    @commands.command(name="quote")
    async def get_quote(self, ctx):
        quote = self.quotes[random.choice(list(self.quotes.keys()))]
        embed = discord.Embed(title=quote["quote"], colour=discord.Colour(0x9013fe),
                              description=f"- {quote['author']}, {quote['year']}")

        await ctx.send(embed=embed)

    @commands.command(name="addquote")
    async def add_quote(self, ctx, quote: str, author: str, year: str):
        db.reference("quotes").push({
            "quote": quote,
            "author": author,
            "year": year
        })

        self.quotes = db.reference("quotes").get()
        await ctx.send(f"{ctx.message.author.mention} Quote added!")
        await ctx.message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Quotes(bot))

