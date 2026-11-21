from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    ticket_id: int = Field(gt=0)
    ticket_type: str = Field(min_length=1, max_length=80)
    quantity: int = Field(ge=1, le=200)


class OrderAccepted(BaseModel):
    order_id: str
    status: str
    message: str


class OrderView(BaseModel):
    id: str
    ticket_id: int
    ticket_name: str
    ticket_type: str
    quantity: int
    total: float
    location: Optional[str] = None
    organizer: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    dt_event: datetime
    active: bool
    status: str
    stage: str
    reason: Optional[str] = None
    processed_by: Optional[str] = None
    created_at: datetime
    refunded: int = 0
    notifications: list[str] = []


class RefundAccepted(BaseModel):
    refund_id: str
    status: str
    message: str