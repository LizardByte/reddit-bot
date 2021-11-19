import os
import random
import re
import requests
import socket
import sys
import time

import praw
from praw.util.token_manager import FileTokenManager

# database
import pprint
import shelve

# local imports
import keep_alive

# modify as required
VERSION = 'v0'
REDDIT_USER = 'ReenigneArcher'
REFRESH_TOKEN_FILENAME = "refresh_token"


def initialize_refresh_token_file():
    if os.path.isfile(REFRESH_TOKEN_FILENAME):
        return
    
    """Provide the program's entry point when directly executed."""
    scope_input = input(
        "Enter a comma separated list of scopes, or `*` for all scopes: "
    )
    scopes = [scope.strip() for scope in scope_input.strip().split(",")]

    reddit = praw.Reddit(
        redirect_uri='https://%s.%s.repl.co' % (os.environ['REPL_SLUG'], os.environ['REPL_OWNER'].lower()),
        user_agent=USER_AGENT,
    )
    state = str(random.randint(0, 65000))
    url = reddit.auth.url(scopes, state, "permanent")
    print(f"Now open this url in your browser: {url}")

    client, data = receive_connection()
    #data = client.recv(1024).decode("utf-8")
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params = {
        key: value for (key, value) in [token.split("=") for token in param_tokens]
    }

    if state != params["state"]:
        send_message(
            client,
            f"State mismatch. Expected: {state} Received: {params['state']}",
        )
        return 1
    elif "error" in params:
        send_message(client, params["error"])
        return 1

    refresh_token = reddit.auth.authorize(params["code"])
    with open ('refresh_token', 'w+') as f:
        f.write(refresh_token)
    
    send_message(client, f"Refresh token: received from Reddit")
    print('Refresh token has been written to file: ')
    return 0


def receive_connection():
    """Wait for and then return a connected socket..

    Opens a TCP connection on port 8080, and waits for a single client.

    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 8080))
    server.listen()
    # Handle one request from client
    while(True):
        (clientSocket, clientAddress) = server.accept();
        data = clientSocket.recv(1024);
        #print("At Server: %s"%data);

        if(data != b''):
            #Wait until we receive the data from reddit
            if data.startswith(b'GET /?state='):
                # Send back what you received
                clientSocket.send(data);

                break;
    server.close()
    return clientSocket, data.decode("utf-8")


def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()


def get_repl_avatar(user_name):
    url = f'https://replit.com/@{user_name}'
    repl_page = requests.get(url)

    image_link = re.search(r'property=\"og:image\" content=\"(https://storage\.googleapis\.com/replit/images/[a-z_0-9]*\.png)\"', repl_page.text).group(1)

    return image_link


def main():
    if "praw_client_id" not in os.environ:
        sys.stderr.write("Environment variable ``praw_client_id`` must be defined\n")
        return 1
    if "praw_client_secret" not in os.environ:
        sys.stderr.write(
            "Environment variable ``praw_client_secret`` must be defined\n"
        )
        return 1
    
    # replit avatar
    global repl_avatar
    repl_avatar = get_repl_avatar(os.environ['REPL_OWNER'])
    
    # verify reddit refresh token or get new
    initialize_refresh_token_file()

    #keep the server alive
    keep_alive.keep_alive()

    refresh_token_manager = FileTokenManager(REFRESH_TOKEN_FILENAME)

    global reddit
    reddit = praw.Reddit(
        token_manager=refresh_token_manager,
        user_agent=USER_AGENT,
    )
    
    subreddit = reddit.subreddit(os.environ['praw_subreddit'])
    #subreddit = reddit.subreddit("AskReddit")  # testing only

    #process submissions and then keep monitoring
    for submission in subreddit.stream.submissions():
        process_submission(submission)
    
    #process submissions and end
    '''
    for submission in subreddit.new():
        process_submission(submission)
    '''


def process_submission(submission):

    last_online = get_last_online()

    if last_online < submission.created_utc:
        print(submission.id)
        print(submission.title)
        print('---------')

        with shelve.open('reddit_bot_database') as db:
            try:
                db[submission.id]
                submission_exists = True
            except KeyError:
                submission_exists = False
                db[submission.id] = vars(submission)
                #pprint.pprint(vars(submission))
            
            if submission_exists:
                for k, v in vars(submission).items():  # update the database with current values
                    try:
                        if db[submission.id][k] != v:
                            db[submission.id][k] = v
                    except KeyError:
                        db[submission.id][k] = v
            
            else:
                try:
                    os.environ['discord_webhook']
                    db = discord(db, submission)
                except KeyError:
                    pass
                db = flair(db, submission)
                db = karma(db, submission)
    
    # re-write the last online time
    last_online_writer()


def discord(db, submission):
    
    # get the flair color
    try:
        color = int(submission.link_flair_background_color, 16)
    except:
        color = int('ffffff', 16)

    try:
        redditor = reddit.redditor(name=submission.author)
    except:
        return

    ### actually send the message... to do
    discord_webhook = {
        'username' : os.environ['REPL_SLUG'],
        'avatar_url' : repl_avatar,
        'embeds': [
            {
            'author': {
                'name': str(submission.author),
                'url': 'https://www.reddit.com/user/%s' % (submission.author),
                'icon_url': str(redditor.icon_img)
                },
            'title': str(submission.title),
            'url': str(submission.url),
            'description': str(submission.selftext),
            'color': color,
            'thumbnail': {
                'url': 'https://www.redditstatic.com/desktop2x/img/snoo_discovery@1x.png'
                },
            'footer': {
                'text': 'Posted on r/%s at %s' % (os.environ['praw_subreddit'], submission.created_utc),
                'icon_url': 'https://www.redditstatic.com/desktop2x/img/favicon/favicon-32x32.png'
                }
            }
        ]
    }

    r = requests.post(os.environ['discord_webhook'], json=discord_webhook)
    print(r.status_code)
    print(type(r.status_code))

    if r.status_code == 204:  # successful completion of request, no additional content
        # update the database
        db[submission.id]['bot_discord'] = {'sent' : True, 'sent_utc': int(time.time())}

    return db

def flair(db, submission):
    # do stuff
    return db


def karma(db, submission):
    # do stuff
    return db


def commands(db, submission):
    # do stuff
    return db


def last_online_writer():
    last_online = int(time.time())
    with open ('last_online', 'w') as f:
        f.write(str(last_online))

    return last_online


def get_last_online():
    try:
        with open ('last_online', 'r') as f:
            last_online = int(f.read())
    except FileNotFoundError:
        last_online = last_online_writer()
    
    return last_online


USER_AGENT='%s/%s by u/%s' % (os.environ['REPL_SLUG'], VERSION, REDDIT_USER)

if __name__ == "__main__":
    main()
