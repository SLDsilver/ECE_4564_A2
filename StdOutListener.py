#ECE4674T18 c:Squires+Wishes
#ECE4674T18 p:Squires+Wishes “I wish I had gotten their number.”

#p:Squires+Wishes #ECE4674T18 “I wish I had gotten their number.”
#p:Squires+Wishes “I wish I had gotten their number.” #ECE4674T18"

#c:Squires+Wishes #ECE4674T18

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Credentials
consumer_key = '2ARmDBxpFU49b0gBTLid5g9Ct'
consumer_secret = 'KKCfwGSJPNLbaMqtVroP4nbsManKwyksIylTwAKLL561aRgKjc'
access_token = '1033783380171796480-Zx62vbm5FjQZ3jI5iedrSH2VJ0kjQk'
access_token_secret = 'kgbWibpppTBgFSnNZPkzTmhbp3gmQnAHqdfNlrqvXEDtP'

class StdOutListener(StreamListener):
    def on_status(self, status):
        if not 'RT @' in status.text:

            First = status.text.split()
            if First[0][0] == '#':
                if len(First) == 2:
                    sub1 = First[1].split("+")
                    print(sub1[0][0]) #Action
                    print(sub1[0][2:len(sub1[0])]) #Place
                    print(sub1[1]) #Subject
                else:
                    sub1 = First[1].split("+")
                    print(sub1[0][0]) #Action
                    print(sub1[0][2:len(sub1[0])]) #Place
                    print(sub1[1]) #Subject
                    count = 2
                    Message = ''
                    while count < len(First):
                        Message = Message + First[count] + ' '
                        count += 1
                    print(Message) #Message
            elif First[0][0] == 'p':
                sub1 = First[0].split("+")
                print(sub1[0][0]) #Action
                print(sub1[0][2:len(sub1[0])])  #Place
                print(sub1[1]) #Subject
                Message = ''
                if First[1][0] == '#':
                    count = 2
                    while count < len(First):
                        Message = Message + First[count] + ' '
                        count += 1
                    print(Message) #Message
                else:
                    count = 1
                    while count < (len(First) - 1):
                        Message = Message + First[count] + ' '
                        count += 1
                    print(Message) #Message
            else:
                sub1 = First[0].split("+")
                print(sub1[0][0])  #Action
                print(sub1[0][2:len(sub1[0])])  #Place
                print(sub1[1]) #Subject

        return



l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

while True:
    try:
        stream.filter(track=["#ECE4674T18"])
    except:
        continue
