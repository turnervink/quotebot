# Purple Empire Quote Bot

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
`BOT_TOKEN` is the Discord bot token