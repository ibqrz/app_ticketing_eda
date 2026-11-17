from uuid import UUID

from fastapi import APIRouter, Query

from common.messaging.publisher import EventPublisher
from repositories.events import EventRepository
from repositories.orders import OrderRepository
from schemas.orders import OrderAccepted, OrderCreate, OrderView
from services.orders import OrderService

router = APIRouter(prefix="/api/orders", tags=["orders"])

service = OrderService(OrderRepository(), EventRepository(), EventPublisher())


@router.post("", response_model=OrderAccepted, status_code=202)
def create(data: OrderCreate):
    return service.create(data)


@router.get("", response_model=list[OrderView])
def recent(limit: int = Query(10, ge=1, le=50)):
    return service.recent(limit)


@router.get("/{order_id}", response_model=OrderView)
def find(order_id: UUID):
    return service.find(str(order_id))
