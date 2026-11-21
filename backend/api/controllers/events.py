from fastapi import APIRouter

from repositories.events import EventRepository
from schemas.events import EventView
from services.events import EventService

router = APIRouter(prefix="/api/events", tags=["events"])

service = EventService(EventRepository())


@router.get("", response_model=list[EventView])
def all():
    return service.all()