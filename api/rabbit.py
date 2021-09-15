import json
import pika
from config import Config

def send_message(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=Config.RABBIT_HOST,
            port=Config.RABBIT_PORT
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue=Config.RABBIT_QUEUE, durable=True, auto_delete=False)


    channel.basic_publish(
        exchange="",
        routing_key=Config.RABBIT_QUEUE,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()