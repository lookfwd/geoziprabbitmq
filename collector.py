#!/usr/bin/env python

import random
import pika
import sys
import json


HOST = 'rabbitmq-123456.cont.dockerapp.io'
PORT = 32771

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=HOST, port=PORT))
channel = connection.channel()

channel.queue_declare(queue='done_postcode', durable=True)


def done_postcode(ch, method, properties, body):
    my_resp = json.loads(body)

    postcode = my_resp['postcode']
    viewport = my_resp['viewport']

    entry = {postcode: viewport}

    with open("test.txt", "a") as myfile:
        myfile.write(json.dumps(entry) + "\n")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(done_postcode, queue='done_postcode')
channel.start_consuming()
