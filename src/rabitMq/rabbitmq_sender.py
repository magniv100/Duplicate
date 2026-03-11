#!/usr/bin/env python
import pika
import logging

def send_message(message):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='rabbitmq1')

    channel.basic_publish(exchange='', routing_key='rabbitmq1', body=message)
    logging.info("Message sent")
    connection.close()