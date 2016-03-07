#!/usr/bin/env python

import random
import pika
import sys
import json

HOST = 'rabbitmq-123456.cont.dockerapp.io'
PORT = 32771

with open('sources.json', 'r') as f:
    postcodes = json.loads(f.read())

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=HOST, port=PORT))
    channel = connection.channel()

    channel.queue_declare(queue='todo_postcode', durable=True)

    for postcode in postcodes:
        channel.basic_publish(exchange='',
                              routing_key='todo_postcode',
                              body=postcode,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
