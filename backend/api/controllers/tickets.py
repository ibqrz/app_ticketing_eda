from fastapi import APIRouter
from fastapi.responses import FileResponse

from common.errors import NotFoundError
from container import attachments, ticket_service
from schemas.tickets import TicketView

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


@router.get("", response_model=list[TicketView])
def listing():
    return ticket_service.listing()


@router.get("/{ticket_id}/image")
def image(ticket_id: int):
    path = attachments.find(ticket_id)
    if path is None:
        raise NotFoundError("Imagem não encontrada.")
    return FileResponse(path, headers={"Cache-Control": "public, max-age=3600"})
