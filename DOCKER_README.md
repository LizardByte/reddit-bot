# Docker

## Using docker run
Create and run the container (substitute your `<values>`):

```bash
docker run -d \
  --name=lizardbyte-reddit-bot \
  --restart=unless-stopped \
  -e PRAW_CLIENT_ID=<PRAW_CLIENT_ID> \
  -e PRAW_CLIENT_SECRET=<PRAW_CLIENT_SECRET> \
  -e PRAW_SUBREDDIT=<PRAW_SUBREDDIT> \
  -e DISCORD_WEBHOOK=<DISCORD_WEBHOOK> \
  -e GRAVATAR_EMAIL=<GRAVATAR_EMAIL> \
  -e REDIRECT_URI=<REDIRECT_URI> \
  -p 8080:8080 \
  lizardbyte/reddit-bot
```

To update the container it must be removed and recreated:

```bash
# Stop the container
docker stop lizardbyte-reddit-bot
# Remove the container
docker rm lizardbyte-reddit-bot
# Pull the latest update
docker pull lizardbyte/reddit-bot
# Run the container with the same parameters as before
docker run -d ...
```

## Using docker-compose

Create a `docker-compose.yml` file with the following contents (substitute your `<values>`):

```yaml
version: '3'
services:
  lizardbyte-reddit-bot:
    image: lizardbyte/reddit-bot
    container_name: lizardbyte-reddit-bot
    restart: unless-stopped
    environment:
      - PRAW_CLIENT_ID=<PRAW_CLIENT_ID>
      - PRAW_CLIENT_SECRET=<PRAW_CLIENT_SECRET>
      - PRAW_SUBREDDIT=<PRAW_SUBREDDIT>
      - DISCORD_WEBHOOK=<DISCORD_WEBHOOK>
      - GRAVATAR_EMAIL=<GRAVATAR_EMAIL>
      - REDIRECT_URI=<REDIRECT_URI>
    ports:
      - 8080:8080
```

Create and start the container (run the command from the same folder as your `docker-compose.yml` file):

```bash
docker-compose up -d
```

To update the container:
```bash
# Pull the latest update
docker-compose pull
# Update and restart the container
docker-compose up -d
```

## Parameters
You must substitute the `<values>` with your own settings.

Parameters are split into two halves separated by a colon. The left side represents the host and the right side the
container.

**Example:** `-p external:internal` - This shows the port mapping from internal to external of the container.
Therefore `-p 8080:8080` would expose port `8080` from inside the container to be accessible from the host's IP on port
`8080` (e.g. `http://<host_ip>:8080`). The internal port must be `8080`, but the external port may be changed
(e.g. `-p 8181:8080`).

| Parameter          | Required | Default | Description                                                             |
|--------------------|----------|---------|-------------------------------------------------------------------------|
| PRAW_CLIENT_ID     | True     | None    | `client_id` from reddit app setup page.                                 |
| PRAW_CLIENT_SECRET | True     | None    | `client_secret` from reddit app setup page.                             |
| PRAW_SUBREDDIT     | True     | None    | Subreddit to monitor (reddit user should be moderator of the subreddit) |
| DISCORD_WEBHOOK    | False    | None    | URL of webhook to send discord notifications to                         |
| GRAVATAR_EMAIL     | False    | None    | Gravatar email address to get avatar from                               |
| REDIRECT_URI       | True     | None    | The redirect URI entered during the reddit application setup            |

Further instructions can be found in the main [readme](https://github.com/LizardByte/reddit-bot/blob/master/README.md).
