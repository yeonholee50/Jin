from flask import request, Response
from pymongo import MongoClient
import os
import slack

client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))

def list_items():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    connection_string = os.getenv('MONGO_DB')
    mongo_client = MongoClient(connection_string)
    db = mongo_client.sample
    collection = db.added
    cursor = collection.find({'user_id': user_id})
    if not cursor:
        client.chat_postMessage(channel=channel_id, text='Your list is currently empty.')
    else:
        complete_text = ""
        count = 1
        for doc in cursor:
            complete_text = complete_text + str(count) + '. ' + doc['text'] + '\n'
            count += 1
        client.chat_postMessage(channel=channel_id, text=complete_text)
    mongo_client.close()
    return Response(), 200
