import logging
from decimal import Decimal
from uuid import uuid4

from common.errors import NotFoundError, UnavailableError
from common.events import ORDER_CREATED, OrderEvent

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, orders, tickets, publisher):
        self.orders = orders
        self.tickets = tickets
        self.publisher = publisher

    def create(self, user, data):
        row, kind = self.tickets.sellable(data.ticket_id, data.ticket_type)
        total = (Decimal(str(kind["price"])) * data.quantity).quantize(Decimal("0.01"))
        event = OrderEvent(
            order_id=str(uuid4()),
            user_id=user["id"],
            ticket_id=row["id"],
            ticket_type=kind["name"],
            quantity=data.quantity,
            total=total,
            customer_name=user["name"],
            customer_email=user["email"],
        )
        self.orders.add(event)
        try:
            self.publisher.publish(ORDER_CREATED, event.to_dict())
        except Exception as error:
            logger.exception("publish failed for order %s", event.order_id)
            self.orders.remove(event.order_id)
            raise UnavailableError("Serviço de mensageria indisponível.") from error
        return {
            "order_id": event.order_id,
            "status": "PROCESSING",
            "message": "Pedido Recebido / Em Processamento",
        }

    def find(self, user, order_id):
        order = self.orders.find(order_id, user["id"])
        if order is None:
            raise NotFoundError("Pedido não encontrado.")
        order["notifications"] = self.orders.notifications(order_id)
        return order

    def recent(self, user, scope, limit):
        return self.orders.recent(user["id"], scope, limit)
