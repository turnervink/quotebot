import discord
import pytz


def get_quote_date(message: discord.Message):
    localized_date = pytz.timezone("US/Pacific").localize(message.created_at)
    return localized_date.strftime("%-d %B, %Y")
    # TODO Interpret user input and format consistently
