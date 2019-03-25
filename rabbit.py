#!/usr/bin/env python
import pika
import sys

class Messenger:
    def __init__(self,host='localhost'):
        #Set host
        self.host = host
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

    def getQueue(self, place, subject):
        return self.queue_names[place][self.exchanges[place].index(subject)]

    def produce(self,place,subject,message):
        self.channel.basic_publish(exchange=place, routing_key=subject, body=message)

    def consume_callback(self, ch, method, properties, body):
        #Print out everything
        print("Place: ", str(method.exchange))
        print("Subject: ", str(method.routing_key))
        print("Message: ", str(body))

    def consume(self,place,subject):
        self.channel.basic_consume(self.consume_callback,queue=self.getQueue("Squires","Food"),no_ack=True)
        self.channel.basic_consume(self.consume_callback,queue=self.getQueue("Squires","Rooms"),no_ack=True)

        self.channel.start_consuming()

if __name__=="__main__":
    msg1 = Messenger()
    msg2 = Messenger()

    msg1.produce("Squires","Food","Im Hungry damnit")
    msg1.produce("Squires","Rooms","Embeddi boi")
    msg2.consume("Squires","Food")
