import logging
import time

import pika
from pika.exceptions import AMQPConnectionError

from common.config import settings

logger = logging.getLogger(__name__)


def connect(attempts=30, delay=2):
    parameters = pika.URLParameters(settings.rabbitmq_url)
    parameters.heartbeat = 60
    for attempt in range(1, attempts + 1):
        try:
            return pika.BlockingConnection(parameters)
        except AMQPConnectionError:
            logger.warning("broker unavailable, attempt %s/%s", attempt, attempts)
            time.sleep(delay)
    raise ConnectionError("broker unavailable")
