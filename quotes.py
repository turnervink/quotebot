import discord
from discord.ext import commands

import db

from datetime import datetime, timedelta
import os
import random

# How long the cooldown period is
COOLDOWN_PERIOD_SECONDS = int(os.environ["COOLDOWN_PERIOD_SECONDS"])

# The number of times a user can issue the get quote command within the penalty window before hitting a cooldown
MAX_GET_QUOTE_INVOCATIONS_BEFORE_COOLDOWN = int(os.environ["MAX_GET_QUOTE_INVOCATIONS_BEFORE_COOLDOWN"])

# If a user issues the get quote command again within this period they get one invocation closer to a cooldown
# If they wait longer than this period their invocations reset to 1
GET_QUOTE_PENALTY_WINDOW_SECONDS = int(os.environ["GET_QUOTE_PENALTY_WINDOW_SECONDS"])


class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quotes = db.get_quotes()
        self.invocations = {}
        self.cooldowns = {}

    def user_is_in_cooldown(self, user: discord.User):
        try:
            if datetime.now() < self.cooldowns[user.id]:
                return True
            else:
                return False
        except KeyError:
            return False

    def start_cooldown(self, user: discord.User):
        self.cooldowns[user.id] = datetime.now() + timedelta(seconds=COOLDOWN_PERIOD_SECONDS)
        self.invocations[user.id]["count"] = 0

    @commands.slash_command(name="quote", description="Get a random quote")
    async def get_quote(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if self.user_is_in_cooldown(ctx.author):
            await ctx.followup.send(f"You're doing that too much {ctx.author.mention}! Try again in a bit.")
            return

        try:
            user_invocation_count = self.invocations[ctx.author.id]["count"]
            user_last_invocation_time = self.invocations[ctx.author.id]["last_invocation"]

            if user_invocation_count == MAX_GET_QUOTE_INVOCATIONS_BEFORE_COOLDOWN and\
                    datetime.now() - user_last_invocation_time < timedelta(seconds=GET_QUOTE_PENALTY_WINDOW_SECONDS):
                self.start_cooldown(ctx.author)
                self.invocations[ctx.author.id]["last_invocation"] = datetime.now()
                await ctx.followup.send(f"You're doing that too much {ctx.author.mention}! Try again in a bit.")
                return
            else:
                if datetime.now() - user_last_invocation_time < timedelta(seconds=GET_QUOTE_PENALTY_WINDOW_SECONDS):
                    self.invocations[ctx.author.id]["count"] = user_invocation_count + 1
                else:
                    self.invocations[ctx.author.id]["count"] = 1

                self.invocations[ctx.author.id]["last_invocation"] = datetime.now()
        except KeyError:
            self.invocations[ctx.author.id] = {
                "count": 1,
                "last_invocation": datetime.now()
            }

        if self.quotes is not None:
            quote = self.quotes[random.choice(list(self.quotes.keys()))]

            embed = discord.Embed(title=quote["quote"], colour=discord.Colour(0x9013fe),
                                  description=f"- {quote['author']} | {quote['date']}")
            await ctx.followup.send(embed=embed)
        else:
            await ctx.followup.send("You haven't created any quotes yet! Add one with **/addquote**.")

    @commands.slash_command(name="search", description="Search for a quote")
    async def search_for_quote(
            self,
            ctx: discord.ApplicationContext,
            contents_substr: discord.Option(str, name="text", description="The quote text to search for", required=False, default=""),
            author: discord.Option(str, description="The name of the quote author", required=False, default=None)
    ):
        await ctx.defer()
        if contents_substr is None and author is None:
            await ctx.followup.send("You need to specify at least one of `text` or `author` in your search")
            return

        quotes = []

        for key in self.quotes.keys():
            if author is not None:
                if self.quotes[key]["author"].lower() == author.lower():
                    quotes.append(self.quotes[key])
            else:
                quotes.append(self.quotes[key])

        matching_quotes = [quote for quote in quotes if contents_substr.lower() in quote["quote"].lower()]

        results_list = ""
        for quote in matching_quotes:
            results_list += f"\"{quote['quote']}\" - {quote['author']}, {quote['date']}\n\n"

        embed = discord.Embed(title="Search results", colour=discord.Colour(0x9013fe),
                              description=results_list)
        await ctx.followup.send(embed=embed)

    @commands.slash_command(name="addquote", description="Add a quote")
    async def add_quote(
            self,
            ctx: discord.ApplicationContext,
            quote: discord.Option(str, description="The quote text"),
            author: discord.Option(str, description="The author's name"),
            date: discord.Option(str, description="The date the quote was said")
    ):
        await ctx.defer()
        db.push_quote(quote, author, date)
        self.quotes = db.get_quotes()
        await ctx.followup.send(f"{ctx.author.mention} Quote added!")

    @commands.slash_command(name="refresh", description="Refresh the quotes from the database")
    async def refresh_cached_quotes(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        self.quotes = db.get_quotes()
        await ctx.followup.send("Quotes refreshed!")


def setup(bot: commands.Bot):
    bot.add_cog(Quotes(bot))
