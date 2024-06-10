import discord
from discord.ext import commands
from discord.ext.pages import Paginator, Page

import db
import util

import os

# How long the cooldown period is
COOLDOWN_PERIOD_SECONDS = int(os.environ["COOLDOWN_PERIOD_SECONDS"])

# The number of times a user can issue the get quote command within the penalty window before hitting a cooldown
COOLDOWN_MAX_INVOCATIONS = int(
    os.environ["COOLDOWN_MAX_INVOCATIONS"])


class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.postgres = db.Postgres(
            os.environ["POSTGRES_HOST"],
            os.environ["POSTGRES_PORT"],
            os.environ["POSTGRES_DATABASE"],
            os.environ["POSTGRES_USERNAME"],
            os.environ["POSTGRES_PASSWORD"]
        )

    @commands.slash_command(name="quote", description="Get a random quote")
    @commands.cooldown(COOLDOWN_MAX_INVOCATIONS, COOLDOWN_PERIOD_SECONDS, commands.BucketType.user)
    async def get_quote(self, ctx: discord.ApplicationContext):
        quote = self.postgres.get_random_quote()

        if quote is None:
            await ctx.respond("No quotes found")
            return

        embed = util.build_quote_embed(
            quote["quote"], quote["author"], quote["freeform_date"])

        await ctx.respond(embed=embed)

    @commands.slash_command(name="addquote", description="Add a quote")
    async def add_quote(
            self,
            ctx: discord.ApplicationContext,
            quote: discord.Option(str, description="The quote text"),
            author: discord.Option(str, description="The author's name"),
            date: discord.Option(
                str, description="The date the quote was said")
    ):
        self.postgres.add_quote(quote, author, date)
        await ctx.respond("Quote added!")

    @commands.slash_command(name="search", description="Search for a quote")
    async def search_quotes(
        self,
        ctx: discord.ApplicationContext,
        search_term: discord.Option(str, name="text", description="The quote text to search for", required=False, default=None),
        author: discord.Option(
            str, description="The name of the quote author", required=False, default=None)
    ):
        total_matches = self.postgres.get_total_search_matches(
            search_term, author
        )

        if total_matches == 0:
            await ctx.respond("No quotes found")
            return

        total_pages = (total_matches // db.PAGE_SIZE) + 1

        quote_pages = []
        for page in range(1, total_pages + 1):
            quotes = self.postgres.search_quotes(search_term, author, page)

            embed = discord.Embed(colour=discord.Colour(util.EMBED_COLOUR))
            for quote in quotes:
                embed.add_field(
                    name=quote["quote"], value=f"{quote['author']} | {quote['freeform_date']}", inline=False
                )

            quote_pages.append(Page(embeds=[embed]))

        quotes_paginator = Paginator(quote_pages)
        await quotes_paginator.respond(ctx.interaction)


def setup(bot: commands.Bot):
    bot.add_cog(Quotes(bot))
