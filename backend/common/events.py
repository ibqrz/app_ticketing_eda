from dataclasses import asdict, dataclass, replace
from decimal import Decimal, InvalidOperation
from typing import Optional
from uuid import UUID

from common.errors import InvalidMessageError

ORDER_CREATED = "order.created"
STOCK_RESERVED = "stock.reserved"
STOCK_SOLD_OUT = "stock.sold_out"
PAYMENT_APPROVED = "payment.approved"
PAYMENT_REFUSED = "payment.refused"
TICKET_REFUND_REQUESTED = "ticket.refund_requested"
TICKET_REFUNDED = "ticket.refunded"


@dataclass(frozen=True)
class OrderEvent:
    order_id: str
    user_id: int
    ticket_id: int
    ticket_type: str
    quantity: int
    total: Decimal
    customer_name: str
    customer_email: str
    reason: Optional[str] = None

    @classmethod
    def parse(cls, payload):
        if not isinstance(payload, dict):
            raise InvalidMessageError("payload must be a JSON object")
        try:
            event = cls(
                order_id=str(UUID(str(payload["order_id"]))),
                user_id=int(payload["user_id"]),
                ticket_id=int(payload["ticket_id"]),
                ticket_type=str(payload["ticket_type"]).strip(),
                quantity=int(payload["quantity"]),
                total=Decimal(str(payload["total"])),
                customer_name=str(payload["customer_name"]).strip(),
                customer_email=str(payload["customer_email"]).strip(),
                reason=payload.get("reason"),
            )
        except (KeyError, TypeError, ValueError, InvalidOperation) as error:
            raise InvalidMessageError(f"invalid payload: {error!r}") from error
        event.check()
        return event

    def check(self):
        if self.quantity < 1 or self.ticket_id < 1 or self.user_id < 1:
            raise InvalidMessageError("quantity, ticket_id and user_id must be positive")
        if not self.total.is_finite() or self.total <= 0:
            raise InvalidMessageError("total must be a positive number")
        if not self.ticket_type or not self.customer_name or not self.customer_email:
            raise InvalidMessageError("ticket type and customer data are required")

    def to_dict(self):
        data = asdict(self)
        data["total"] = str(self.total)
        return data

    def with_reason(self, reason):
        return replace(self, reason=reason)


@dataclass(frozen=True)
class RefundEvent:
    refund_id: str
    order_id: str
    user_id: int
    ticket_id: int
    ticket_type: str
    amount: Decimal
    customer_name: str
    customer_email: str

    @classmethod
    def parse(cls, payload):
        if not isinstance(payload, dict):
            raise InvalidMessageError("payload must be a JSON object")
        try:
            event = cls(
                refund_id=str(UUID(str(payload["refund_id"]))),
                order_id=str(UUID(str(payload["order_id"]))),
                user_id=int(payload["user_id"]),
                ticket_id=int(payload["ticket_id"]),
                ticket_type=str(payload["ticket_type"]).strip(),
                amount=Decimal(str(payload["amount"])),
                customer_name=str(payload["customer_name"]).strip(),
                customer_email=str(payload["customer_email"]).strip(),
            )
        except (KeyError, TypeError, ValueError, InvalidOperation) as error:
            raise InvalidMessageError(f"invalid payload: {error!r}") from error
        event.check()
        return event

    def check(self):
        if self.ticket_id < 1 or self.user_id < 1:
            raise InvalidMessageError("ticket_id and user_id must be positive")
        if not self.amount.is_finite() or self.amount <= 0:
            raise InvalidMessageError("amount must be a positive number")
        if not self.ticket_type or not self.customer_name or not self.customer_email:
            raise InvalidMessageError("ticket type and customer data are required")

    def to_dict(self):
        data = asdict(self)
        data["amount"] = str(self.amount)
        return data