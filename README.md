# Quote Bot
Lets you store funny and weird things your friends say and retrieve them randomly
so you can laugh at them out of context

## Development
- Set the following local environment variables
```
# The token for your Discord bot
BOT_TOKEN=<discord bot token>

# Database information for local development
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=<postgres database name>
POSTGRES_USERNAME=<postgres username>
POSTGRES_PASSWORD=<postgres password>

# Command cooldown values
COOLDOWN_MAX_INVOCATIONS=<N>
COOLDOWN_PERIOD_SECONDS=<N>

# An option list of integer Discord server IDs to create the bot's commands on
# Speeds up development by limiting how many servers need to have commands set up
DEBUG_GUILD_IDS='[]'
```
- Create the `pgdata` directory in the repo directory
- `docker-compose -f docker-compose.local.yml up` to spin up a Postgres container that can be accessed outside of the container
- Install dependencies with `poetry install`
- `poetry run python src/bot.py` to start the bot

## Deployment
- Create a `.env` file and set the environment variables as needed for your production environment
- Use `docker compose up` to start the bot's container stack on your production machine
