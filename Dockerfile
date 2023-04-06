FROM python:3.11.3-slim-bullseye

# Secret config
ARG PRAW_CLIENT_ID
ARG PRAW_CLIENT_SECRET
ARG PRAW_SUBREDDIT
ARG DISCORD_WEBHOOK
ARG GRAVATAR_EMAIL
ARG REDIRECT_URI

# Environment variables
ENV PRAW_CLIENT_ID=$PRAW_CLIENT_ID
ENV PRAW_CLIENT_SECRET=$PRAW_CLIENT_SECRET
ENV PRAW_SUBREDDIT=$PRAW_SUBREDDIT
ENV DISCORD_WEBHOOK=$DISCORD_WEBHOOK
ENV GRAVATAR_EMAIL=$GRAVATAR_EMAIL
ENV REDIRECT_URI=$REDIRECT_URI

# create data directory
RUN mkdir -p /data
VOLUME /data

RUN mkdir -p /app
WORKDIR /app/

COPY requirements.txt .
COPY *.py .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "reddit_bot.py"]
