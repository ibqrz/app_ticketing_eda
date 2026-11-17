import json
import logging
import uuid

import pika

from common.messaging.connection import connect
from common.messaging.topology import EXCHANGE, declare_topology

logger = logging.getLogger(__name__)


class EventPublisher:
    def publish(self, routing_key, body):
        connection = connect(attempts=3, delay=1)
        try:
            channel = connection.channel()
            declare_topology(channel)
            channel.confirm_delivery()
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json",
                    message_id=str(uuid.uuid4()),
                ),
                mandatory=True,
            )
            logger.info("published %s", routing_key)
        finally:
            connection.close()
