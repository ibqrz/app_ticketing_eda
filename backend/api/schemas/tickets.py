from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TypeView(BaseModel):
    name: str
    price: float


class TicketView(BaseModel):
    id: int
    name: str
    description: str
    organizer: str
    location: str
    dt_event: datetime
    dt_expiration: Optional[datetime] = None
    dt_finished: Optional[datetime] = None
    sales_end: datetime
    types: list[TypeView]
    available: int
    image: Optional[str] = None
    status: bool
    open: bool
    sold_out: bool
