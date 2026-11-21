from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from container import order_service
from controllers.dependencies import current_user
from schemas.orders import OrderAccepted, OrderCreate, OrderView, RefundAccepted

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderAccepted, status_code=202)
def create(data: OrderCreate, user=Depends(current_user)):
    return order_service.create(user, data)


@router.get("", response_model=list[OrderView])
def recent(
    scope: Literal["purchased", "tracking"] = "purchased",
    limit: int = Query(10, ge=1, le=100),
    user=Depends(current_user),
):
    return order_service.recent(user, scope, limit)


@router.get("/{order_id}", response_model=OrderView)
def find(order_id: UUID, user=Depends(current_user)):
    return order_service.find(user, str(order_id))


@router.post("/{order_id}/refunds", response_model=RefundAccepted, status_code=202)
def refund(order_id: UUID, user=Depends(current_user)):
    return order_service.refund(user, str(order_id))
