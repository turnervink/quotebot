import discord
from discord.ext import commands

import db

from datetime import datetime, timedelta
import random


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

    @commands.command(name="quote")
    async def get_quote(self, ctx):
        if self.user_is_in_cooldown(ctx.message.author):
            await ctx.send(f"You're doing that too much {ctx.message.author.mention}! Try again later.")
        else:
            quote = self.quotes[random.choice(list(self.quotes.keys()))]
            embed = discord.Embed(title=quote["quote"], colour=discord.Colour(0x9013fe),
                                  description=f"- {quote['author']} | {quote['date']}")
            await ctx.send(embed=embed)

            user_num_invocations = self.invocations.get(ctx.message.author.id)
            if user_num_invocations is None:
                self.invocations[ctx.message.author.id] = 1
            elif user_num_invocations == 2:  # This is the user's 3rd invocation since their last cooldown
                self.cooldowns[ctx.message.author.id] = datetime.now() + timedelta(minutes=3)
                self.invocations[ctx.message.author.id] = 0
            else:
                self.invocations[ctx.message.author.id] = user_num_invocations + 1

    @commands.command(name="addquote")
    async def add_quote(self, ctx, quote: str, author: str, date: str):
        db.push_quote(quote, author, date)
        self.quotes = db.get_quotes()
        await ctx.send(f"{ctx.message.author.mention} Quote added!")
        await ctx.message.delete()

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(title="Quote Bot Help")
        embed.add_field(name="Get a quote:", value="`$quote`", inline=False)
        embed.add_field(name="Add a new quote:",
                        value="`$addquote \"Your cool quote\" \"Author Name\" \"January 1st, 1970\"`", inline=False)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Quotes(bot))
