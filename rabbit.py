#!/usr/bin/env python
import pika
import sys

class Messenger:
    def __init__(self,host='localhost'):
        #Set host
        self.host = host
        self.queue_name = "Messages"
        #Instantiate rabbitmq connection and channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        #Declare exchanges and queues
        places = ["Squires","Goodwin","Library"]
        exchanges = dict()
        exchanges["Squires"] = ["Food","Meetings","Rooms"]
        exchanges["Goodwin"] = ["Classrooms","Auditorium"]
        exchanges["Library"] = ["Noise","Seating","Wishes"]

        for place in places:
            print("Declaring Exchange: ", place)
            self.shannel.exchange_declare(exchange=place,type='direct')

            for key in exchanges[place]:
                print("\tBinding Queue: ", key)
                self.channel.queue_bind(exchange=place,queue=self.queue_name,routing_key=key)



    def produce(self,place,subject,message):
        channel.basic_publish(exchange=place,
                              routing_key=subject,
                              body=message)

    def consume_callback(self, ch, method, properties, body):
        #Return array [Action Place Subject Message]
        return ["",str(method.routing_key),str(method.exchange),str(body)]

    def consume(self,place,subject):

if __name__=="__main__":
    msg = Messenger()
