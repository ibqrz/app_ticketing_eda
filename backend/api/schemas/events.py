from datetime import datetime

from pydantic import BaseModel


class TicketView(BaseModel):
    id: int
    name: str
    price: float
    available: int


class EventView(BaseModel):
    id: int
    title: str
    venue: str
    city: str
    starts_at: datetime
    tickets: list[TicketView]