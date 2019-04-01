#!/usr/bin/env python
import pika
import sys

class Messenger:
    def __init__(self,host='localhost',version='c'):
        #Set host
        self.prevtag = ''
        self.credentials = pika.PlainCredentials('admin', 'password')
        self.host = host
        self.prevplace = ''
        self.prevsubject = ''
        self.consumers = []
        #Instantiate rabbitmq connection and channel
        ########################## STUDY INFORMATION #################################
        #To use rabbitmq, which is just a glorified message queue, you first have to set up the server
        #the server is set up and configured on the system as an apt-get install,it should not be
        #on the test. There is usually a sereis of users with different permissions, our system uses
        #a user called admin with the password password, which has univerasl rights. You can see the PlainCredentials
        #used to access the remote server above

        #This function call creates a persistant blocking connection to the remote server described in the paragraph above
        #this comment.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,port=5672,credentials=self.credentials))
        #This line creates a channel on the connection made before, think of the connection as a doorway and this channel as an object
        #that carries information through the doorway
        self.channel = self.connection.channel()
        ###############################################################################
        #Declare exchanges and queues
        #Here all that is being set up is stuff that is assignm,ent specific, no need to worry about this for study purposes
        places = ["Squires","Goodwin","Library"]
        self.exchanges = dict()
        self.exchanges["Squires"] = ["Food","Meetings","Rooms"]
        self.exchanges["Goodwin"] = ["Classrooms","Auditorium"]
        self.exchanges["Library"] = ["Noise","Seating","Wishes"]
        self.queue_names = dict()
        self.queue_names["Squires"] = ["Food","Meetings","Rooms"]
        self.queue_names["Goodwin"] = ["Classrooms","Auditorium"]
        self.queue_names["Library"] = ["Noise","Seating","Wishes"]
        self.info_exchange = ''

        if version == 'r':
            ###########################  STUDY INFORMATION #############################
            #In this part of the code, a single exchange with a single queue is being set up,
            #for refrence, this section is setting up the exchange to handle consume requests,
            #It tells the system to consume one of the quqes, something I explain further down

            #This line uses the channel to create an exchange on the rabbit server
            #exchanges are effectively nodes that can have multiple queues within them
            #The part of this line that may be changed for the examn is the echange name "Consume_Requests"
            self.channel.exchange_declare(exchange="Consume_Requests",exchange_type='direct')
            #Here a queue is created in the previosly created exchange, this queue has an automatically generated name,
            #to specify the name of a queue if you want to know what it is exactly, you can pass an argument queue="name"
            #we do this in the for loop below this study information block if you want an example of it.
            self.info_exchange = self.channel.queue_declare(exclusive=True).method.queue
            #Here the queue that was declared is assigned to the aforementioned exchange, kind of linking them together.
            #There is also a routing key which can be used to bind multiple queues with the same name to a single exchange
            #The slides have an example where this is used, but we haver a single queue for each subject of info.
            self.channel.queue_bind(exchange="Consume_Requests",queue=self.info_exchange,routing_key="Key")
            #Just noticed this duplicate line, it doesnt do much but we submitted it so fuck it
            self.channel.queue_bind(exchange="Consume_Requests",queue=self.info_exchange,routing_key="Key")

            #Here we are creating a consumer, what the consumer does is looks at its specifically assigned quque and
            #preforms a user defined callback on anything that shows up in the queue, this occurs on ly when the enire channel is in
            #'consume mode' i will call it. Which is instantiated by calling channel.start_consuming()
            #see the next study information block for information regarding the callback
            self.channel.basic_consume(self.info_callback,queue=self.info_exchange,no_ack=True)

            #############################################################################
            for place in places:
                #print("Declaring Exchange: ", place)
                self.channel.exchange_declare(exchange=place,exchange_type='direct')

                for key in self.exchanges[place]:
                    #declare new quque with name
                    self.channel.queue_declare(exclusive=True,queue=key)
                    queue_name = key#result.method.queue

                    #print("\tBinding Queue: ", key)
                    self.channel.queue_bind(exchange=place,queue=queue_name,routing_key=key)

            self.channel.start_consuming()

    def produce(self,place,subject,message):
        ###################################### STUDY INFORMATION #################################
        #This is how you send information to a queue in an exchange. Basically you just publish a string to
        #an existing queue, you need to know the name of the exchange, and the name of the queue that you want
        #to publish to. This is where the different routhing keys can come in if you need them. We dont use it
        #in our project so they are all set to "Key" for simplicity.
        print("[Checkpoint] Produce Request Recieved in RabbitMQ Queue")
        if(message == "Consume Request"):
            new_body = place + " " + subject
            self.channel.basic_publish(exchange="Consume_Requests", routing_key="Key", body=new_body)
        else:
            self.channel.basic_publish(exchange=place, routing_key=subject, body=message)
        ##########################################################################################
    def info_callback(self, ch, method, properties, body):
        ###########################  STUDY INFORMATION #############################
        #This is a callback that is called every time an assigned consumer gets something
        #in its specifig queue. The arguments here are all required (other than self if it is not in a class)
        #basically you can do anyhting you want in here, the tools you have to operate with are in the
        #method object:

        #method.exchange gives you the exchange this callback was called from
        #method.routing_key gives you the key that was used
        #body is the body of the message that was givn note that body is a bitstream

        #there are many other things that can be used, they are clear in the rabbit doccumentation
        info = body.split()
        self.consume(info[0].decode(),info[1].decode())
        ############################################################################
    def consume_callback(self, ch, method, properties, body):
        #Print out everything
        new_thread = False
        place = str(method.exchange)
        subject = str(method.routing_key)

        if place != self.prevplace:
            print("\nPlace: ", place)
            self.prevplace = place
            new_thread = True
        if subject != self.prevsubject:
            print("Subject: ", subject)
            self.prevsubject = subject
            new_thread = True
        if new_thread:
            print("\tMessages: ", body.decode())
        else:
            print("\t          ", body.decode())

    def consume(self,place,subject):
        print("[Checkpoint] Consume Request Recieved in RabbitMQ Queue")
        self.channel.basic_cancel(self.prevtag)
        self.prevtag =  self.channel.basic_consume(self.consume_callback,queue=subject,no_ack=True)
        #self.channel.start_consuming()

if __name__=="__main__":
    #This will never be called it is for testing
    msg1 = Messenger(host='192.168.1.104')

    msg1.produce("Squires","Food","Im Hungry")
    msg1.produce("Squires","Rooms","Embeddi boi")
    msg1.produce("Goodwin","Classrooms","Diffeq Here")
    msg1.produce("Goodwin","Auditorium","Consume Request")
