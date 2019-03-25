#ECE4674T10 c:Squires+Wishes
#ECE4674T10 p:Squires+Wishes “I wish I had gotten their number.”

#p:Squires+Wishes #ECE4674T10 “I wish I had gotten their number.”
#p:Squires+Wishes “I wish I had gotten their number.” #ECE4674T10"

#c:Squires+Wishes #ECE4674T10

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
from gpiozero import LED
from pymongo import MongoClient
from captureKeys import *

redLED = LED(17)
greenLED = LED(27)
blueLED = LED(22)

class StdOutListener(StreamListener):

    def on_status(self, status):
        self.Action = ''
        self.Place = ''
        self.Subject = ''
        self.Message = ''
        
        if not 'RT @' in status.text:
            First = status.text.split()
            if First[0][0] == '#':
                if len(First) == 2:
                    sub1 = First[1].split("+")
                    self.Action = sub1[0][0] #Action
                    self.Place = sub1[0][2:len(sub1[0])] #Place
                    self.Subject = sub1[1] #Subject
                else:
                    sub1 = First[1].split("+")
                    self.Action = sub1[0][0] #Action
                    self.Place = sub1[0][2:len(sub1[0])] #Place
                    self.Subject = sub1[1] #Subject
                    count = 2
                    while count < len(First):
                        self.Message = self.Message + First[count] + ' '
                        count += 1
            elif First[0][0] == 'p':
                sub1 = First[0].split("+")
                self.Action = sub1[0][0] #Action
                self.Place = sub1[0][2:len(sub1[0])]  #Place
                self.Subject = sub1[1] #Subject
                if First[1][0] == '#':
                    count = 2
                    while count < len(First):
                        self.Message = self.Message + First[count] + ' '
                        count += 1
                else:
                    count = 1
                    while count < (len(First) - 1):
                        self.Message = self.Message + First[count] + ' '
                        count += 1
            else:
                sub1 = First[0].split("+")
                self.Action = sub1[0][0]  #Action
                self.Place = sub1[0][2:len(sub1[0])] #Place
                self.Subject = sub1[1] #Subject
                
            client = MongoClient('localhost', 27017)
            db = client.team_10
            post = {}
                
            if (self.Action == "p"):
                post = {
                    "Action": "p",
                    "Place": self.Place,
                    "msgID": "10$" + str(time.time()),
                    "Subject": self.Subject,
                    "Message": self.Message
                    }
                greenLED.off()
                blueLED.off()
                time.sleep(1)
            elif (self.Action == "c"):
                post = {
                    "Action": "c",
                    "Place": self.Place,
                    "msgID": "10$" + str(time.time()),
                    "Subject": self.Subject
                    }
                redLED.off()
                blueLED.off()
                time.sleep(1)
                
            if post:
                posts = db.posts
                post_id = posts.insert_one(post).inserted_id

        redLED.on()
        greenLED.on()
        blueLED.on()
        
        return


l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

redLED.on()
greenLED.on()
blueLED.on()

while True:
    try:
        stream.filter(track=["#ECE4674T10"])
    except:
        continue