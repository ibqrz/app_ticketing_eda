from common.errors import InvalidMessageError
from common.events import ORDER_CREATED, PAYMENT_APPROVED, PAYMENT_REFUSED, OrderEvent

KEYS = (ORDER_CREATED, PAYMENT_APPROVED, PAYMENT_REFUSED)


class NotificationController:
    def __init__(self, service):
        self.service = service

    def handle(self, key, payload):
        if key not in KEYS:
            raise InvalidMessageError(f"unexpected routing key {key}")
        self.service.notify(key, OrderEvent.parse(payload))
