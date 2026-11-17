import logging

from common.events import STOCK_RESERVED, STOCK_SOLD_OUT

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(self, repository, publisher):
        self.repository = repository
        self.publisher = publisher

    def reserve(self, event):
        status = self.repository.reserve(
            event.order_id, event.ticket_type_id, event.quantity
        )
        key = STOCK_SOLD_OUT if status == "SOLD_OUT" else STOCK_RESERVED
        logger.info("order %s stock %s", event.order_id, status)
        self.publisher.publish(key, event.to_dict())

    def confirm(self, event):
        self.repository.confirm(event.order_id)
        logger.info("order %s stock confirmed", event.order_id)

    def release(self, event):
        self.repository.release(event.order_id)
        logger.info("order %s stock released", event.order_id)
