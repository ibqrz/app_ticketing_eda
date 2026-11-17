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


@dataclass(frozen=True)
class OrderEvent:
    order_id: str
    ticket_type_id: int
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
                ticket_type_id=int(payload["ticket_type_id"]),
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
        if self.quantity < 1 or self.ticket_type_id < 1:
            raise InvalidMessageError("quantity and ticket_type_id must be positive")
        if not self.total.is_finite() or self.total <= 0:
            raise InvalidMessageError("total must be a positive number")
        if not self.customer_name or not self.customer_email:
            raise InvalidMessageError("customer data is required")

    def to_dict(self):
        data = asdict(self)
        data["total"] = str(self.total)
        return data

    def with_reason(self, reason):
        return replace(self, reason=reason)
