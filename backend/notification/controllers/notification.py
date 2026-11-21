from common.errors import InvalidMessageError
from common.events import (
    ORDER_CREATED,
    PAYMENT_APPROVED,
    PAYMENT_REFUSED,
    TICKET_REFUNDED,
    OrderEvent,
    RefundEvent,
)

KEYS = (ORDER_CREATED, PAYMENT_APPROVED, PAYMENT_REFUSED, TICKET_REFUNDED)


class NotificationController:
    def __init__(self, service):
        self.service = service

    def handle(self, key, payload):
        if key not in KEYS:
            raise InvalidMessageError(f"unexpected routing key {key}")
        parser = RefundEvent if key == TICKET_REFUNDED else OrderEvent
        self.service.notify(key, parser.parse(payload))
