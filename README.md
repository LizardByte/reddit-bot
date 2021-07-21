# RetroArcher.reddit-bot
Reddit bot written in python to help manage the RetroArcher subreddit.

## Instructions
* Setup an application at [reddit apps](https://www.reddit.com/prefs/apps/).
* For the redirecet uri enter `https://<REPL_SLUG>.<REPL_OWNER>.repl.co`
* Take note of the `client_id` and `client_secret`
* Enter the following into the repl secrets
  * praw_client_id = `client_id` from reddit app setup page
  * praw_client_secret = `client_secret` from reddit app setup page
  * praw_subreddit = subreddit to monitor (reddit user should be moderator of the subreddit)
  * discord_webhook = url of webhook to send discord notifications to (optional)
* First run (or manually get a new refresh token):
  * Delete `refresh_token` file if needed
  * `python reddit_bot.py`
  * Open browser and login to reddit account to use with bot
  * Navigate to URL printed in console and accept
  * `refresh_token` file is written
* Running after refresh_token already obtained:
  * `python reddit_bot.py`

## To Do:
Initial functions to add
- [x] Monitor new posts and send a message to a discord channel
- [ ] Monitor new posts and depending on the flair assigned do some checks
  - [ ] reply with a comment if required
  - [ ] lock the post if required (no log file url when using `Help` flair)
- [ ] Monitor comments for specific commands and reply with a specific comment
  - [ ] Intention is to be similar to discord slash commands
- [ ] Monitor new posts and comments, if user has 0 karma, delete the post/comment and send the user a message about why it was deleted

Maybe later on add these type of tasks
- [ ] Count/track how many times a user makes a new post with each flair
- [ ] Count/track how many times users comment on posts that are not their own (will help me identify knowledgable users)
- [ ] other moderation tasks
