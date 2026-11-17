from common.errors import InvalidMessageError
from common.events import ORDER_CREATED, PAYMENT_APPROVED, PAYMENT_REFUSED, OrderEvent


class InventoryController:
    def __init__(self, service):
        self.service = service

    def handle(self, key, payload):
        event = OrderEvent.parse(payload)
        if key == ORDER_CREATED:
            self.service.reserve(event)
        elif key == PAYMENT_APPROVED:
            self.service.confirm(event)
        elif key == PAYMENT_REFUSED:
            self.service.release(event)
        else:
            raise InvalidMessageError(f"unexpected routing key {key}")
