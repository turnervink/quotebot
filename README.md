# Quote Bot
Lets you store funny and weird things your friends say and retrieve them randomly
so you can laugh at them out of context

## Development
- Clone the repo
- Add a file containing your Firebase service account auth info named `db-creds.json` to the root project directory
- Build the Docker image
```
docker build . -t pe-quote-bot:latest
```
- Run the Docker image, passing in the needed arguments
```
docker run -v $(pwd)/db-creds.json:/etc/firebase/db-creds.json -e GOOGLE_APPLICATION_CREDENTIALS=/etc/firebase/db-creds.json -e DB_AUTH_UID=<FIREBASE AUTH UID> -e BOT_TOKEN=<DISCORD BOT TOKEN> pe-quote-bot:latest
```
`GOOGLE_APPLICATION_CREDENTIALS` specifies the path to the DB creds file within the Docker image    
`DB_AUTH_UID` is the unique identifier used to authenticate requests to Firebase  
`DB_ROOT` is the root node of the database to use (e.g. `dev` or `deploy`)  
`BOT_TOKEN` is the Discord bot token  
`BACKUP_DIR` is a local directory on the bot's server to back up quotes to  
`COOLDOWN_PERIOD_SECONDS` is how long the command cooldown period should be  
`MAX_GET_QUOTE_INVOCATIONS_BEFORE_COOLDOWN` is how many times a user can use the get quote command before being put into a cooldown  
`GET_QUOTE_PENALTY_WINDOW_SECONDS` is the window of time that using the get quote command again will count as a usage for determining the cooldown
(e.g if the user uses the command once, then again within this window, their usage count goes up by one)  
`DEBUG_GUILD_IDS` is an array of integer Discord Guild IDs that the bot will create slash commands in, if this is empty commands will be created globally