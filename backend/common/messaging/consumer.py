import json
import logging
import time

from pika.exceptions import AMQPConnectionError

from common.config import settings
from common.errors import InvalidMessageError, RejectedMessage
from common.messaging.connection import connect
from common.messaging.topology import declare_topology

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self, queue, handler):
        self.queue = queue
        self.handler = handler

    def run(self):
        while True:
            try:
                self.listen()
            except AMQPConnectionError:
                logger.warning("connection lost, reconnecting")
                time.sleep(3)
            except KeyboardInterrupt:
                return

    def listen(self):
        connection = connect()
        channel = connection.channel()
        declare_topology(channel)
        channel.basic_qos(prefetch_count=settings.prefetch)
        channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.receive,
            auto_ack=False,
        )
        logger.info("waiting for messages on %s", self.queue)
        channel.start_consuming()

    def decode(self, body):
        try:
            return json.loads(body)
        except ValueError as error:
            raise InvalidMessageError("body is not valid JSON") from error

    def receive(self, channel, method, properties, body):
        key = method.routing_key
        try:
            self.handler(key, self.decode(body))
        except (InvalidMessageError, RejectedMessage) as error:
            logger.warning("%s rejected: %s", key, error)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception:
            logger.exception("%s failed", key)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)
