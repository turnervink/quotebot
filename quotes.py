import discord
from discord.ext import commands, bridge

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

    @bridge.bridge_command(name="quote")
    async def get_quote(self, ctx):
        print('get_quote')

        if self.user_is_in_cooldown(ctx.message.author):
            await ctx.send(f"You're doing that too much {ctx.message.author.mention}! Try again in a bit.")
            return

        try:
            user_invocation_count = self.invocations[ctx.message.author.id]["count"]
            user_last_invocation_time = self.invocations[ctx.message.author.id]["last_invocation"]

            if user_invocation_count == MAX_GET_QUOTE_INVOCATIONS_BEFORE_COOLDOWN and\
                    datetime.now() - user_last_invocation_time < timedelta(seconds=GET_QUOTE_PENALTY_WINDOW_SECONDS):
                self.start_cooldown(ctx.message.author)
                self.invocations[ctx.message.author.id]["last_invocation"] = datetime.now()
                await ctx.send(f"You're doing that too much {ctx.message.author.mention}! Try again in a bit.")
                return
            else:
                if datetime.now() - user_last_invocation_time < timedelta(seconds=GET_QUOTE_PENALTY_WINDOW_SECONDS):
                    self.invocations[ctx.message.author.id]["count"] = user_invocation_count + 1
                else:
                    self.invocations[ctx.message.author.id]["count"] = 1

                self.invocations[ctx.message.author.id]["last_invocation"] = datetime.now()
        except KeyError:
            self.invocations[ctx.message.author.id] = {
                "count": 1,
                "last_invocation": datetime.now()
            }

        quote = self.quotes[random.choice(list(self.quotes.keys()))]
        embed = discord.Embed(title=quote["quote"], colour=discord.Colour(0x9013fe),
                              description=f"- {quote['author']} | {quote['date']}")
        await ctx.send(embed=embed)

    @commands.command(name="search")
    async def search_for_quote(self, ctx, contents_substr: str, author: str = None):
        quotes = []

        for key in self.quotes.keys():
            if author is not None:
                if self.quotes[key]["author"].lower() == author:
                    quotes.append(self.quotes[key])
            else:
                quotes.append(self.quotes[key])

        matching_quotes = [quote for quote in quotes if contents_substr.lower() in quote["quote"].lower()]

        results_list = ""
        for quote in matching_quotes:
            results_list += f"\"{quote['quote']}\" - {quote['author']}, {quote['date']}\n\n"

        embed = discord.Embed(title="Search results", colour=discord.Colour(0x9013fe),
                              description=results_list)
        await ctx.send(embed=embed)

    @commands.command(name="addquote")
    async def add_quote(self, ctx, quote: str, author: str, date: str):
        db.push_quote(quote, author, date)
        self.quotes = db.get_quotes()
        await ctx.send(f"{ctx.message.author.mention} Quote added!")
        await ctx.message.delete()

    @commands.command(name="refresh")
    async def refresh_cached_quotes(self, ctx):
        self.quotes = db.get_quotes()
        await ctx.send("Quotes refreshed!")

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(title="Quote Bot Help")
        embed.add_field(name="Get a quote:", value="`$quote`", inline=False)
        embed.add_field(name="Add a new quote:",
                        value="`$addquote \"Your cool quote\" \"Author Name\" \"January 1st, 1970\"`", inline=False)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Quotes(bot))
