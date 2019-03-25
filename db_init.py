#!/usr/bin/env python3
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.team_10
collection = db.tweets

post = {
    "Action": "p",
    "Place": "Squires",
    "msgID": "10$1476123693.1855621",
    "Subject": "Rooms",
    "Message": "I like the comfortable chairs on the 3rd floor"
    }

posts = db.posts
post_id = posts.insert_one(post).inserted_id