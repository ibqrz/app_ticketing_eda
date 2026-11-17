import logging
from uuid import uuid4

from common.errors import NotFoundError, UnavailableError
from common.events import ORDER_CREATED, OrderEvent

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, orders, events, publisher):
        self.orders = orders
        self.events = events
        self.publisher = publisher

    def create(self, data):
        ticket = self.events.ticket(data.ticket_type_id)
        if ticket is None:
            raise NotFoundError("ticket type not found")
        event = OrderEvent(
            order_id=str(uuid4()),
            ticket_type_id=ticket["id"],
            quantity=data.quantity,
            total=ticket["price"] * data.quantity,
            customer_name=data.customer_name.strip(),
            customer_email=data.customer_email,
        )
        self.orders.add(event)
        try:
            self.publisher.publish(ORDER_CREATED, event.to_dict())
        except Exception as error:
            logger.exception("publish failed for order %s", event.order_id)
            self.orders.remove(event.order_id)
            raise UnavailableError("message broker unavailable") from error
        return {
            "order_id": event.order_id,
            "status": "PROCESSING",
            "message": "Pedido Recebido / Em Processamento",
        }

    def find(self, order_id):
        order = self.orders.find(order_id)
        if order is None:
            raise NotFoundError("order not found")
        order["notifications"] = self.orders.notifications(order_id)
        return order

    def recent(self, limit):
        return self.orders.recent(limit)
