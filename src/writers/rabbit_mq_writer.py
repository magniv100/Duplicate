import pika
import logging


async def rabbit_mq_writer(message):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='rabbitmq1')

    channel.basic_publish(exchange='', routing_key='rabbitmq1', body=message)
    logging.info("Message sent")
    connection.close()
