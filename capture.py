from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
from gpiozero import LED
from pymongo import MongoClient
from captureKeys import *
import rabbit as rb
import argparse as ap

redLED = LED(17)
greenLED = LED(27)
blueLED = LED(22)

class Capture(StreamListener):
    def __init__(self,host='localhost',tag='#ECE4564T10',cp=False):
        StreamListener.__init__(self)
        self.host = "".join(host)
        self.messenger = rb.Messenger(self.host)
        self.hashtag = tag

    def on_status(self, status):
        self.Action = ''
        self.Place = ''
        self.Subject = ''
        self.Message = ''

        if not 'RT @' in status.text:
            if self.cp: print("[Checkpoint] Tweet Captured: ", status.text)
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

            client = MongoClient(self.host, 27017)
            db = client.team_10
            if (self.Place == "Squires"): db = client.Squires
            elif (self.Place == "Goodwin"): db = client.Goodwin
            elif (self.Place == "Library"): db = client.Library
            post = {}

            if (self.Action == "p"):
                post = {
                    "Action": "p",
                    "Place": self.Place,
                    "msgID": "10$" + str(time.time()),
                    "Subject": self.Subject,
                    "Message": self.Message
                    }
                self.messenger.produce(self.Place,self.Subject,self.Message)
                if self.cp: print("[Checkpoint] Produce Request Placed in RabbitMQ Queue")
                greenLED.off()
                blueLED.off()
                if self.cp: print("[Checkpoint] LED Changed to RED")
                time.sleep(1)
            elif (self.Action == "c"):
                post = {
                    "Action": "c",
                    "Place": self.Place,
                    "msgID": "10$" + str(time.time()),
                    "Subject": self.Subject
                    }
                self.messenger.produce(self.Place,self.Subject,"Consume Request")
                if self.cp: print("[Checkpoint] Consume Request Placed in RabbitMQ Queue")
                redLED.off()
                blueLED.off()
                if self.cp: print("[Checkpoint] LED Changed to GREEN")
                time.sleep(1)

            if post:
                posts = db.posts
                if (self.Subject == "Food"): posts = db.Food
                elif (self.Subject == "Meetings"): posts = db.Meetings
                elif (self.Subject == "Rooms"): posts = db.Rooms
                elif (self.Subject == "Classrooms"): posts = db.Classrooms
                elif (self.Subject == "Auditorium"): posts = db.Auditorium
                elif (self.Subject == "Noise"): posts = db.Noise
                elif (self.Subject == "Seating"): posts = db.Seating
                elif (self.Subject == "Wishes"): posts = db.Wishes
                post_id = posts.insert_one(post).inserted_id
                if self.cp: print("[Checkpoint] Command Stored in MongoDB: ", post)


        redLED.on()
        greenLED.on()
        blueLED.on()
        if self.cp: print("[Checkpoint] LED Changed to WHITE")

        return

def monitor(listener,hashtag):
    l = listener
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    while True:
        try:
            stream.filter(track=[hashtag])
        except:
            continue

if __name__ == '__main__':
    parser = ap.ArgumentParser(description="Launch the capture module for Assignemnt 2")

    parser.add_argument('-s',action='store',dest='IP',type=str,nargs='+',help="IP server is hosted on, default localhost",default='localhost',required=False)
    parser.add_argument('-t',action='store',dest='hashtag',type=str,nargs='+',help="Hashtag being searched for",default="#ECE4564T10",required=False)
    parser.add_argument('--silent',action='store_true',dest='silent',help="Disable checkopoint output, enabled by default",default=True,required=False)

    args = parser.parse_args()

    redLED.on()
    greenLED.on()
    blueLED.on()

    capture = Capture(host=args.IP,tag=args.hashtag,cp=args.silent)

    monitor(capture,args.hashtag)
