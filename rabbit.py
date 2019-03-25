#!/usr/bin/env python
import pika
import sys

class Messenger:
    def __init__(self,host='localhost'):
        #Set host
        self.host = host
        self.prevplace = ''
        self.prevsubject = ''
        #Instantiate rabbitmq connection and channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
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

        for place in places:
            print("Declaring Exchange: ", place)
            self.channel.exchange_declare(exchange=place,exchange_type='direct')

            for key in self.exchanges[place]:
                #declare new quque with name
                result = self.channel.queue_declare(exclusive=True)
                queue_name = result.method.queue
                self.queue_names[place].append(queue_name)

                print("\tBinding Queue: ", key)
                self.channel.queue_bind(exchange=place,queue=queue_name,routing_key=key)

    def produce(self,place,subject,message):
        self.channel.basic_publish(exchange=place, routing_key=subject, body=message)

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

    def consume(self):
        for key, value in self.queue_names.items():
            for q in value:
                self.channel.basic_consume(self.consume_callback,queue=str(q),no_ack=True)
        self.channel.start_consuming()

if __name__=="__main__":
    msg1 = Messenger()
    msg2 = Messenger()

    msg1.produce("Squires","Food","Im Hungry damnit")
    msg1.produce("Squires","Rooms","Embeddi boi")
    msg1.produce("Goodwin","Classrooms","Diffeq HW Due?")
    msg2.consume()
