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
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,port=5672,credentials=self.credentials))
        self.channel = self.connection.channel()
        #Declare exchanges and queues
        places = ["Squires","Goodwin","Library"]
        self.exchanges = dict()
        self.exchanges["Squires"] = ["Food","Meetings","Rooms"]
        self.exchanges["Goodwin"] = ["Classrooms","Auditorium"]
        self.exchanges["Library"] = ["Noise","Seating","Wishes"]
        self.queue_names = dict()
        self.queue_names["Squires"] = []
        self.queue_names["Goodwin"] = []
        self.queue_names["Library"] = []
        self.info_exchange = ''

        if version == 'r':
            self.channel.exchange_declare(exchange="Consume_Requests",exchange_type='direct')
            self.info_exchange = self.channel.queue_declare(exclusive=True).method.queue
            self.channel.queue_bind(exchange="Consume_Requests",queue=self.info_exchange,routing_key="Key")

            self.channel.queue_bind(exchange="Consume_Requests",queue=self.info_exchange,routing_key="Key")
            self.channel.basic_consume(self.info_callback,queue=self.info_exchange,no_ack=True)
            self.channel.start_consuming()
        else:
            for place in places:
                #print("Declaring Exchange: ", place)
                self.channel.exchange_declare(exchange=place,exchange_type='direct')

                for key in self.exchanges[place]:
                    #declare new quque with name
                    result = self.channel.queue_declare(exclusive=True)
                    queue_name = result.method.queue
                    self.queue_names[place].append(queue_name)

                    #print("\tBinding Queue: ", key)
                    self.channel.queue_bind(exchange=place,queue=queue_name,routing_key=key)

    def produce(self,place,subject,message):
        if(message == "Consume Request"):
            new_body = place + " " + subject
            self.channel.basic_publish(exchange="Consume_Requests", routing_key="Key", body=new_body)
        else:
            self.channel.basic_publish(exchange=place, routing_key=subject, body=message)

    def getQueue(self,place,subject):
        return self.queue_names[place][self.exchanges[place].index(subject)]

    def info_callback(self, ch, method, properties, body):
        info = body.split()
        self.consume(info[0],info[1])

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
        self.prevtag = self.getQueue(place,subject)
        self.channel.basic_cancel(self.prevtag)
        self.channel.basic_consume(self.consume_callback,queue=self.getQueue(place,subject),no_ack=True)
        self.channel.start_consuming()

if __name__=="__main__":
    msg1 = Messenger(host='192.168.1.104')
    msg2 = Messenger(host='192.168.1.104')

    msg1.produce("Squires","Food","Im Hungry damnit")
    msg1.produce("Squires","Rooms","Embeddi boi")
    msg1.produce("Goodwin","Classrooms","Diffeq HW Due?")
    msg2.consume("Squires","Food")
