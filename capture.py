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
import rabbit

redLED = LED(17)
greenLED = LED(27)
blueLED = LED(22)

class StdOutListener:
    def __init__(self,host='localhost',tag='#ECE4564T10',cp=False,StreamListener):
        self.messenger = rb.Messenger(self.host)
        self.monitor() #initilize monitering

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
                message = "Produce Request: " + self.Message
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
                message = "Consume Request"
                redLED.off()
                blueLED.off()
                time.sleep(1)

            if post:
                posts = db.posts
                post_id = posts.insert_one(post).inserted_id
                self.messenger.produce(self.Place,self.Subject,message)

        redLED.on()
        greenLED.on()
        blueLED.on()

        return

    def monitor(self):
        while True:
            try:
                stream.filter(track=["#ECE4674T10"])
            except:
                continue

if __name__ == '__main__':
    parser = ap.ArgumentParser(description="Launch the capture module for Assignemnt 2")

    parser.add_argument('-s',action='store',dest='IP',type=str,nargs='+',help="IP server is hosted on, default localhost",default='localhost',required=False)
    parser.add_argument('-t',action='store',dest='hashtag',type=str,nargs='+',help="Hashtag being searched for",default="#ECE4564T10",required=False)
    parser.add_argument('--silent',action='store_true',dest='silent',help="Disable checkopoint output, enabled by default",default=True,required=False)

    args = parser.parse_args()

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    redLED.on()
    greenLED.on()
    blueLED.on()


    capture = Capture(host=args.IP,tag=args.hashtag,cp=args.silent)
