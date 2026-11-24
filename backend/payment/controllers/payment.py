from common.errors import InvalidMessageError
from common.events import STOCK_RESERVED, STOCK_SOLD_OUT, OrderEvent


class PaymentController:
    def __init__(self, service):
        self.service = service

    def handle(self, key, payload):
        event = OrderEvent.parse(payload)
        if key == STOCK_RESERVED:
            self.service.charge(event)
        elif key == STOCK_SOLD_OUT:
            self.service.refuse(event, "SOLD_OUT")
        else:
            raise InvalidMessageError(f"unexpected routing key {key}")