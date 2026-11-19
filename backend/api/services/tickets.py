from datetime import datetime, timedelta, timezone

from common.config import settings
from common.errors import BadRequestError, ConflictError, NotFoundError


def moment(info, key):
    value = info.get(key)
    return datetime.fromisoformat(value) if value else None


def closes_at(info):
    dates = [moment(info, "dtExpiration"), moment(info, "dtEvent")]
    return min(date for date in dates if date)


def is_open(row, now):
    return row["available"] > 0 and now < closes_at(row["info"])


def is_listed(row, now):
    info = row["info"]
    if now >= closes_at(info):
        return False
    if row["available"] > 0:
        return True
    finished = moment(info, "dtFinished")
    if finished is None:
        return True
    return now < finished + timedelta(hours=settings.sold_out_ttl_hours)


class TicketService:
    def __init__(self, repository):
        self.repository = repository

    def listing(self):
        now = datetime.now(timezone.utc)
        return [
            self.view(row, now) for row in self.repository.all() if is_listed(row, now)
        ]

    def view(self, row, now):
        info = row["info"]
        return {
            "id": row["id"],
            "name": info["name"],
            "description": info.get("description", ""),
            "organizer": info.get("organizer", ""),
            "location": info.get("location", ""),
            "dt_event": moment(info, "dtEvent"),
            "dt_expiration": moment(info, "dtExpiration"),
            "dt_finished": moment(info, "dtFinished"),
            "sales_end": closes_at(info),
            "types": info.get("types", []),
            "available": row["available"],
            "image": row["image"],
            "status": now < moment(info, "dtEvent"),
            "open": is_open(row, now),
            "sold_out": row["available"] == 0,
        }

    def sellable(self, ticket_id, type_name):
        row = self.repository.find(ticket_id)
        if row is None:
            raise NotFoundError("Ingresso não encontrado.")
        kind = next(
            (item for item in row["info"].get("types", []) if item["name"] == type_name),
            None,
        )
        if kind is None:
            raise BadRequestError("Tipo de ingresso inválido.")
        if not is_open(row, datetime.now(timezone.utc)):
            raise ConflictError("As vendas deste ingresso estão encerradas.")
        return row, kind
