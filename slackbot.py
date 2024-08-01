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
        text_history_collection.insert_one({
            'channel_id': channel_id,
            'user_id': user_id,
            'text': text,
            'payload': payload
        })

        # Update or insert into count collection
        count_collection = db.count
        user_document = count_collection.find_one({'user_id': user_id, 'channel_id': channel_id})

        if user_document:
            count_collection.find_one_and_update(
                {'user_id': user_id, 'channel_id': channel_id},
                {'$inc': {'count': 1}}
            )
        else:
            count_collection.insert_one({'user_id': user_id, 'channel_id': channel_id, 'count': 1})

        mongo_client.close()

        


        

# will record the message count every time in that specified channel from mongo
@app.route('/message-count', methods=['POST', 'GET'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    connection_string = MONGO_DB
    mongo_client = MongoClient(connection_string)
    db = mongo_client.sample
    collection = db.count
    document = collection.find_one({'user_id': user_id, 'channel_id': channel_id})
    
    if not document:
        client.chat_postMessage(channel=channel_id, text='you have talked for a total of 0 messages in this channel')
    else:
        count = document['count']
        client.chat_postMessage(channel=channel_id, text=f'You have talked for a total of {count} messages in this channel.')
    
    mongo_client.close()
    return Response(), 200
#will return every previous messages in that specified channel from mongo
@app.route('/previous-messages', methods=['POST', 'GET'])
def previous_messages():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    connection_string = MONGO_DB
    mongo_client = MongoClient(connection_string)
    db = mongo_client.sample
    collection = db.text_history
    cursor = collection.find({'user_id': user_id, 'channel_id': channel_id})
    if not cursor:
        client.chat_postMessage(channel=channel_id, text='you have talked for a total of 0 messages in this channel')
    else:
        complete_text = ""
        for doc in cursor:
            complete_text = complete_text + doc['text'] + '\n'
        client.chat_postMessage(channel=channel_id, text=complete_text)
    mongo_client.close()
    return Response(), 200

#will return every command available. ***IMPORTANT***: Please add new commands over here
@app.route('/help', methods=['POST', 'GET'])
def help():
    data = request.form
    name = data['user_name']
    channel_id = data.get('channel_id')
    commands = {
        '• /ping': 'Use this to check if Jin is alive in your channel',
        '• /help': 'Use this to see all the available commands your version of Jin has',
        '• /message-count': 'Use this to see how often you participated in this channel',
        '• /previous-messages': 'Use this to see what you have previously said'
    }
    complete_text = f"Hey {name}. These are the list of commands your current version of Jin supports: \n"
    for command in commands.keys():
        text_to_add = command + ': ' + commands[command] + '\n'
        complete_text = complete_text + text_to_add
    client.chat_postMessage(channel=channel_id, text=complete_text)
    return Response(), 200

#will return every previous messages in that specified channel from mongo
@app.route('/ping', methods=['POST', 'GET'])
def ping():
    data = request.form
    name = data['user_name']
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id, text=f"Hi {name}👋, I'm here.")
    return Response(), 200




if __name__ == "__main__":
    app.run(debug=True)