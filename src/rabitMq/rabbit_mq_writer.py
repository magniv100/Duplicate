import pika
import logging

from fastapi import UploadFile


async def rabbit_mq_writer(image: UploadFile, metadata: dict):
    image_bytes = await image.read()

    metadata['image_type'] = image.content_type

    properties = pika.BasicProperties(headers=metadata, content_type=image.content_type)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='rabbitmq1')

    channel.basic_publish(exchange='', routing_key='rabbitmq1', body=image_bytes, properties=properties)
    logging.info("Message sent")
    connection.close()
