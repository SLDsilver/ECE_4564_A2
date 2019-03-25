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
        exchanges["Squires"] = ["Food","Meetings","Rooms"]
        exchanges["Goodwin"] = ["Classrooms","Auditorium"]
        exchanges["Library"] = ["Noise","Seating","Wishes"]
        self.queue_names = dict()

        for place in places:
            print("Declaring Exchange: ", place)
            self.shannel.exchange_declare(exchange=place,type='direct')

            for key in exchanges[place]:
                #declare new quque with name
                result = channel.queue_declare(exclusive=True)
                queue_name = result.method.queue
                self.queue_names[place].append(queue_name)

                print("\tBinding Queue: ", key)
                self.channel.queue_bind(exchange=place,queue=queue_name,routing_key=key)



    def produce(self,place,subject,message):
        self.channel.basic_publish(exchange=place,
                              routing_key=subject,
                              body=message)

    def consume_callback(self, ch, method, properties, body):
        #Print out everything
        return ["",str(method.routing_key),str(method.exchange),str(body)]

    def consume(self,place,subject):
        self.channel.basic_consume(callback,queue=self.queue_name,no_ack=True)
        self.start_consuming()

if __name__=="__main__":
    msg = Messenger()
