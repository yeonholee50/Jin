import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from environment import SIGNING_SECRET 
from environment import SLACK_TOKEN
from environment import MONGO_DB
from pymongo import MongoClient


app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(SIGNING_SECRET,'/slack/events',app)
client = slack.WebClient(token=SLACK_TOKEN)


BOT_ID = client.api_call("auth.test")['user_id']

@slack_event_adapter.on('message')

def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    

    if user_id != BOT_ID:
        connection_string = MONGO_DB
        mongo_client = MongoClient(connection_string)
        db = mongo_client.sample
        collection = db.data
        result = collection.insert_one({'user_id': user_id, 'text': text})
        print(result)
        mongo_client.close()
        client.chat_postMessage(channel=channel_id, text=text)


if __name__ == "__main__":
    app.run(debug=True)