from flask import request, Response
from pymongo import MongoClient
import os
import slack

client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))

def update_item():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    items = data.get('text').split(':')
    if len(items) != 2:
        client.chat_postMessage(channel=channel_id, text=f"Command is in form /update_item item_to_replace new_item")
        return Response(), 200
    item_text = items[0]
    new_text = items[-1]
    


    connection_string = os.getenv('MONGO_DB')
    mongo_client = MongoClient(connection_string)
    db = mongo_client.sample
    collection = db.added
    
    result = collection.update_one(
        {'user_id': user_id, 'channel_id': channel_id, 'text': item_text},
        {'$set': {'text': new_text}}
    )
    
    if result.modified_count > 0:
        client.chat_postMessage(channel=channel_id, text=f"Updated item: {item_text} to {new_text}.")
    else:
        client.chat_postMessage(channel=channel_id, text=f"Item: {item_text} not found.")
    
    mongo_client.close()
    return Response(), 200
