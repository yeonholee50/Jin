import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import socket
import time
from flask import Flask


app = Flask(__name__)

@app.route("/")
def main():
    
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    
    if client:
        print("Jin has successfully connected")
    else:
        print("Jin has failed to connect")
    while True:
        time.sleep(10)
        client.chat_postMessage(channel="#testbot", text="Hello World")
        print("Hello World Posted")

if __name__ == "__main__":
    
    main()