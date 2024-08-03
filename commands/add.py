from flask import request, Response
from pymongo import MongoClient
import os

def add_item():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    user_text = data.get('text')
    connection_string = os.getenv('MONGO_DB')
    mongo_client = MongoClient(connection_string)
    db = mongo_client.sample
    collection = db.added
    collection.insert_one({
            'channel_id': channel_id,
            'user_id': user_id,
            'text': user_text,
    })
    mongo_client.close()
    return Response(), 200
