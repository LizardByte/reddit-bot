#!/usr/bin/env python

"""This example demonstrates the flow for retrieving a refresh token.

This tool can be used to conveniently create refresh tokens for later use with your web
application OAuth2 credentials.

To create a Reddit application visit the following link while logged into the account
you want to create a refresh token for: https://www.reddit.com/prefs/apps/

Create a "web app" with the redirect uri set to: https://<name of Repl>.<replit username>.repl.co

After the application is created, take note of:

- client id; the line just under "web app" in the upper left of the Reddit
  Application...
     enter this as a secret under the name `praw_client_id`
- client secret; the value to the right of "secret"...
     enter this as a secret under the name `praw_client_secret`
- redirect uri; the value you entered from above...
     enter this as a secret under the name `REDDIT_REDIRECT_URI`

Usage:

    python3 obtain_refresh_token.py


This is only here for reference!
"""

import os
import random
import socket
import sys

import praw


def main():
    if "praw_client_id" not in os.environ:
        sys.stderr.write("Environment variable ``praw_client_id`` must be defined\n")
        return 1
    if "praw_client_secret" not in os.environ:
        sys.stderr.write(
            "Environment variable ``praw_client_secret`` must be defined\n"
        )
        return 1
    
    """Provide the program's entry point when directly executed."""
    scope_input = input(
        "Enter a comma separated list of scopes, or `*` for all scopes: "
    )
    scopes = [scope.strip() for scope in scope_input.strip().split(",")]

    reddit = praw.Reddit(
        redirect_uri=os.environ['REDDIT_REDIRECT_URI'],
        user_agent="obtain_refresh_token/v0 by u/bboe",
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
    
    send_message(client, f"Refresh token: {refresh_token}")
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


if __name__ == "__main__":
    sys.exit(main())
