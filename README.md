# Quotebot
Quotebot is a bot for Discord that lets your store the funny things your friends say and pull up random quotes to look back on out of context.

## Adding Quotebot to Your Server
I make no guarantees about service quality or uptime, since this is a self-hosted project.

Invite the bot with this link:  
https://discord.com/oauth2/authorize?client_id=782829124149444658

## Development
Quotebot uses Python with Poetry for dependency management, and Postgres as a database.

- Clone the project
- Install dependenices with `poetry install`
- Set the following environment variables with your development values:
```
# The token for your Discord bot
BOT_TOKEN=<discord bot token>

# Database information for local development
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=postgres
POSTGRES_USERNAME=<dev postgres username>
POSTGRES_PASSWORD=<dev postgres password>

# Command cooldown values
COOLDOWN_MAX_INVOCATIONS=<N>
COOLDOWN_PERIOD_SECONDS=<N>

# An option list of integer Discord server IDs to create the bot's commands on
# Speeds up development by limiting how many servers need to have commands set up
DEBUG_GUILD_IDS='[]'
```
- Create a `pgdata` directory in the project root
- Start a local database with `docker compose -f docker-compose.local.yml up -d`
- Start the bot with `poetry run python src/bot.py`
- When you're done stop the local database with `docker compose -f docker-compose.local.yml down`

## Deployment
- Create a `.env` file with your production values:
```
# The token for your Discord bot
BOT_TOKEN=<discord bot token>

# Database information
POSTGRES_USERNAME=<dev postgres username>
POSTGRES_PASSWORD=<dev postgres password>

# Command cooldown values
COOLDOWN_MAX_INVOCATIONS=<N>
COOLDOWN_PERIOD_SECONDS=<N>
```
- Build the production image with `docker compose build`
- Use `docker compose up` to start the bot's container stack on your production machine

## Contributing
If you for some reason want to contribute to this silly thing feel free to fork it and open a PR!
