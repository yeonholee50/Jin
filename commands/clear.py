from flask import request, Response
from pymongo import MongoClient
import os
import slack

client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))

def clear_items():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    connection_string = os.getenv('MONGO_DB')
    mongo_client = MongoClient(connection_string)
    db = mongo_client.sample
    collection = db.added
    
    result = collection.delete_many({'user_id': user_id, 'channel_id': channel_id})
    
    client.chat_postMessage(channel=channel_id, text=f"Cleared {result.deleted_count} items from your list.")
    mongo_client.close()
    return Response(), 200
