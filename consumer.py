#!/usr/bin/env python

# Auto start on boot with:
#
# $ cat /etc/init/pygeo.conf
# start on runlevel [2345]
# stop on runlevel [!2345]
#
# exec /home/ubuntu/consumer.py
#
# Create a snapshot and then launch a few instances...
# aws ec2 run-instances --image-id ami-12345 --security-group-ids
# sg-12345 --count 1 --instance-type t2.micro --key-name foobar

import pika
import sys
import json
import time
import requests
from urllib import urlencode

HOST = 'rabbitmq-123456.cont.dockerapp.io'
PORT = 32771
API_KEY = '12345'

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=HOST, port=PORT))
channel = connection.channel()

channel.queue_declare(queue='todo_postcode', durable=True)
channel.queue_declare(queue='done_postcode', durable=True)


def callback(ch, method, properties, postcode):
    try:
        url = ("https://maps.googleapis.com/maps/api/geocode/json?" +
               urlencode({"address": postcode})) + "&key=" + API_KEY
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("can't find")

        resp = r.json()

        viewport = resp["results"][0]["geometry"]["viewport"]

        reply = {
            'postcode': postcode,
            'viewport': viewport
        }

    except:
        reply = {
            'postcode': postcode,
            'viewport': None
        }

    channel.basic_publish(exchange='',
                          routing_key='done_postcode',
                          body=json.dumps(reply),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))

    ch.basic_ack(delivery_tag=method.delivery_tag)

    time.sleep(0.2)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='todo_postcode')
channel.start_consuming()
