#!/usr/bin/env python3

import argparse as ap
import time
from pymongo import MongoClient

class Capture:
    def __init__(self,host='localhost',tag='#ECE4564T10',cp=False):
        self.cp = cp
        self.s = None
        
        command = ["p", "Squires", "Rooms", "I like the comfortable charis on the 3rd floor"]
        self.store_command(command)
        print('success')
        
    def store_command(self, tweet):
        client = MongoClient('localhost', 27017)
        db = client.team_10
        post = {}
        
        if (tweet[0] == "p"):
            post = {
                "Action": tweet[0],
                "Place": tweet[1],
                "msgID": "10$" + str(time.time()),
                "Subject": tweet[2],
                "Message": tweet[3]
                }
        elif (tweet[1] == "c"):
            post = {
                "Action": tweet[0],
                "Place": tweet[1],
                "msgID": "10$" + str(time.time()),
                "Subject": tweet[2]
                }
        
        if post:
            posts = db.posts
            post_id = posts.insert_one(post).inserted_id
        
        
if __name__ == '__main__':
    parser = ap.ArgumentParser(description="Launch the capture module for Assignemnt 2")
    
    parser.add_argument('-s',action='store',dest='IP',type=str,nargs='+',help="IP server is hosted on, default localhost",default='localhost',required=False)
    parser.add_argument('-t',action='store',dest='hashtag',type=str,nargs='+',help="Hashtag being searched for",default="#ECE4564T10",required=False)
    parser.add_argument('--silent',action='store_true',dest='silent',help="Disable checkopoint output, enabled by default",default=True,required=False)
    
    args = parser.parse_args()
    capture = Capture(host=args.IP,tag=args.hashtag,cp=args.silent)