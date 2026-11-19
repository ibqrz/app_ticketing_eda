from fastapi import APIRouter

from container import ticket_service
from schemas.tickets import TicketView

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


@router.get("", response_model=list[TicketView])
def listing():
    return ticket_service.listing()
