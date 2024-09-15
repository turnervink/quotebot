import discord


EMBED_COLOUR = 0x9013fe


def build_quote_embed(quote: str, author: str, date: str) -> discord.Embed:
    return discord.Embed(
        title=quote,
        colour=discord.Colour(EMBED_COLOUR),
        description=f"{author} | {date}"
    )


def humanize_cooldown(seconds: float) -> str:
    rounded = round(seconds)
    if rounded < 60:
        return f"{rounded} {rounded == 1 and 'second' or 'seconds'}"
    elif rounded < 3600:
        return f"{rounded // 60} {rounded // 60 == 1 and 'minute' or 'minutes'}"
    else:
        return f"{rounded // 3600} {rounded // 3600 == 1 and 'hour' or 'hours'}"
