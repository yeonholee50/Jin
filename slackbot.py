import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import socket
import time



def main():
    
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    
    if client:
        print("Jin has successfully connected")
    else:
        print("Jin has failed to connect")
    while True:
        time.sleep(10)
        client.chat_postMessage(channel="#testbot", text="Hello World - from Jin")
        print("Hello World Posted")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('local_host', port))
    main()