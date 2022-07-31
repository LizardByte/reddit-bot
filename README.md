# reddit-bot
Reddit bot written in python to help manage the LizardByte subreddit.

## Instructions
* Set up an application at [reddit apps](https://www.reddit.com/prefs/apps/).
  * The redirect uri must be publicly accessible.
    * If using Replit, enter `https://<REPL_SLUG>.<REPL_OWNER>.repl.co`
    * Otherwise, it is recommended to use [Nginx Proxy Manager](https://nginxproxymanager.com/) and [Duck DNS](https://www.duckdns.org/)
  * Take note of the `client_id` and `client_secret`
* Enter the following as environment variables  

  | Parameter            | Required | Default | Description                                                              |
  | -------------------- | -------- | ------- | ------------------------------------------------------------------------ |
  | PRAW_CLIENT_ID       | True     | None    | `client_id` from reddit app setup page.                                  |
  | PRAW_CLIENT_SECRET   | True     | None    | `client_secret` from reddit app setup page.                              |
  | PRAW_SUBREDDIT       | True     | None    | Subreddit to monitor (reddit user should be moderator of the subreddit)  |
  | DISCORD_WEBHOOK      | False    | None    | URL of webhook to send discord notifications to                          |
  | GRAVATAR_EMAIL       | False    | None    | Gravatar email address to get avatar from                                |
  | REDIRECT_URI         | True     | None    | The redirect URI entered during the reddit application setup             |

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
