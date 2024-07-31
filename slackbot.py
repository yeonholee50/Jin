import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from environment import SIGNING_SECRET 
from environment import SLACK_TOKEN
from environment import MONGO_DB
from pymongo import MongoClient
import copy

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

        # Insert payload into text_history collection
        text_history_collection = db.text_history
        text_history_collection.insert_one(payload)

        # Update or insert into count collection
        count_collection = db.count
        user_document = count_collection.find_one({'user_id': user_id})

        if user_document:
            count_collection.find_one_and_update(
                {'user_id': user_id},
                {'$inc': {'count': 1}}
            )
        else:
            count_collection.insert_one({'user_id': user_id, 'count': 1})

        mongo_client.close()

        


        client.chat_postMessage(channel=channel_id, text=text)

# will record the message count every time in the mongo
@app.route('/message-count', methods=['POST', 'GET'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    text = data.get('text')
    connection_string = MONGO_DB
    mongo_client = MongoClient(connection_string)
    db = mongo_client.sample
    collection = db.count
    cursor = collection.find({'user_id': user_id})
    if not cursor:
        client.chat_postMessage(channel=channel_id, text='0')
    else:
        doc = cursor[0]
        count = doc['count']
        client.chat_postMessage(channel=channel_id, text=f'you have talked for a total of {count}')
    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)