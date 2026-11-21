import logging

from common.errors import RejectedMessage
from common.events import STOCK_RESERVED, STOCK_SOLD_OUT, TICKET_REFUNDED

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(self, repository, publisher):
        self.repository = repository
        self.publisher = publisher

    def reserve(self, event):
        status = self.repository.reserve(
            event.order_id, event.ticket_id, event.quantity
        )
        key = STOCK_SOLD_OUT if status == "SOLD_OUT" else STOCK_RESERVED
        logger.info("order %s stock %s", event.order_id, status)
        self.publisher.publish(key, event.to_dict())

    def confirm(self, event):
        self.repository.confirm(
            event.order_id, event.user_id, event.ticket_id, event.quantity
        )
        logger.info("order %s stock confirmed", event.order_id)

    def release(self, event):
        self.repository.release(event.order_id)
        logger.info("order %s stock released", event.order_id)

    def refund(self, event):
        status = self.repository.refund(event)
        if status == "DENIED":
            raise RejectedMessage(f"refund {event.refund_id} denied")
        if status == "DUPLICATE":
            logger.info("refund %s already processed", event.refund_id)
            return
        logger.info("refund %s stock returned", event.refund_id)
        self.publisher.publish(TICKET_REFUNDED, event.to_dict())
