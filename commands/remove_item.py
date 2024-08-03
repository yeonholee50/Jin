from flask import request, Response
from pymongo import MongoClient
import os
import slack

client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))

def remove_item():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    item_text = data.get('text')
    connection_string = os.getenv('MONGO_DB')
    mongo_client = MongoClient(connection_string)
    db = mongo_client.sample
    collection = db.added
    result = collection.delete_many({'user_id': user_id, 'text': {'$regex': item_text, '$options': 'i'}})
    if result.deleted_count == 0:
        client.chat_postMessage(channel=channel_id, text=f'No items found matching "{item_text}".')
    else:
        client.chat_postMessage(channel=channel_id, text=f'Successfully removed {result.deleted_count} item(s) matching "{item_text}".')
    mongo_client.close()
    return Response(), 200
