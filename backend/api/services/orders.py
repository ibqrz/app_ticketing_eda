import logging
from decimal import Decimal
from uuid import uuid4

from common.errors import ConflictError, NotFoundError, UnavailableError
from common.events import ORDER_CREATED, TICKET_REFUND_REQUESTED, OrderEvent, RefundEvent

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, orders, tickets, publisher, attachments):
        self.orders = orders
        self.tickets = tickets
        self.publisher = publisher
        self.attachments = attachments

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
        return self.decorate(order)

    def recent(self, user, scope, limit):
        return [self.decorate(order) for order in self.orders.recent(user["id"], scope, limit)]

    def decorate(self, order):
        order["image"] = self.attachments.url(order["ticket_id"]) or order["image"]
        return order

    def refund(self, user, order_id):
        order = self.orders.find(order_id, user["id"])
        if order is None:
            raise NotFoundError("Pedido não encontrado.")
        if order["status"] != "CONFIRMED":
            raise ConflictError("Este pedido ainda não foi confirmado.")
        if not order["active"]:
            raise ConflictError("Ingressos de eventos já realizados não podem ser reembolsados.")
        if order["refunded"] >= order["quantity"]:
            raise ConflictError("Todos os ingressos deste pedido já foram reembolsados.")
        amount = (Decimal(order["total"]) / order["quantity"]).quantize(Decimal("0.01"))
        event = RefundEvent(
            refund_id=str(uuid4()),
            order_id=order["id"],
            user_id=user["id"],
            ticket_id=order["ticket_id"],
            ticket_type=order["ticket_type"],
            amount=amount,
            customer_name=user["name"],
            customer_email=user["email"],
        )
        try:
            self.publisher.publish(TICKET_REFUND_REQUESTED, event.to_dict())
        except Exception as error:
            logger.exception("publish failed for refund %s", event.refund_id)
            raise UnavailableError("Serviço de mensageria indisponível.") from error
        return {
            "refund_id": event.refund_id,
            "status": "PROCESSING",
            "message": "Reembolso Solicitado / Em Processamento",
        }
