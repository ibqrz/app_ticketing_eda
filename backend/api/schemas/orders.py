from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class OrderCreate(BaseModel):
    ticket_type_id: int = Field(gt=0)
    quantity: int = Field(ge=1, le=20)
    customer_name: str = Field(min_length=2, max_length=120)
    customer_email: EmailStr


class OrderAccepted(BaseModel):
    order_id: str
    status: str
    message: str


class OrderView(BaseModel):
    id: str
    event_title: str
    ticket_name: str
    quantity: int
    total: float
    status: str
    reason: Optional[str] = None
    processed_by: Optional[str] = None
    created_at: datetime
    notifications: list[str] = []
