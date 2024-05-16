import json

import pika


class RabbitMQ:

    def __init__(self, **kwargs):
        self._host = kwargs["host"]
        self._queue = kwargs["queue"]
        self._connection = None
        self._channel = None

    def _connect(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(self._host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(self._queue)

    def publish(self, **items):
        if not self._connection:
            self._connect()
        elif not self._channel or self._channel.is_closed:
            try:
                self._connection.close()
            finally:
                self._connect()
        self._channel.basic_publish(exchange='', routing_key=items["routing_key"], body=json.dumps(items["body"]))
