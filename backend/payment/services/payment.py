import logging
import time

from common.config import settings
from common.errors import RejectedMessage
from common.events import PAYMENT_APPROVED, PAYMENT_REFUSED

logger = logging.getLogger(__name__)


class PaymentService:
    def __init__(self, repository, publisher):
        self.repository = repository
        self.publisher = publisher

    def charge(self, event):
        time.sleep(settings.processing_delay)
        if event.total > settings.payment_limit:
            self.refuse(event, "LIMIT_EXCEEDED")
            raise RejectedMessage(f"order {event.order_id} above payment limit")
        self.repository.save(
            event.order_id, event.total, "APPROVED", None, settings.instance_id
        )
        logger.info("order %s payment approved", event.order_id)
        self.publisher.publish(PAYMENT_APPROVED, event.to_dict())

    def refuse(self, event, reason):
        self.repository.save(
            event.order_id, event.total, "REFUSED", reason, settings.instance_id
        )
        logger.info("order %s payment refused: %s", event.order_id, reason)
        self.publisher.publish(PAYMENT_REFUSED, event.with_reason(reason).to_dict())