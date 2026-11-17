from common.database import transaction


class EventRepository:
    def all(self):
        with transaction() as cursor:
            cursor.execute(
                "SELECT e.id AS event_id, e.title, e.venue, e.city, e.starts_at, "
                "t.id AS ticket_id, t.name AS ticket_name, t.price, s.available "
                "FROM events e "
                "JOIN ticket_types t ON t.event_id = e.id "
                "JOIN stock_items s ON s.ticket_type_id = t.id "
                "ORDER BY e.starts_at, t.price"
            )
            rows = cursor.fetchall()
        grouped = {}
        for row in rows:
            event = grouped.setdefault(
                row["event_id"],
                {
                    "id": row["event_id"],
                    "title": row["title"],
                    "venue": row["venue"],
                    "city": row["city"],
                    "starts_at": row["starts_at"],
                    "tickets": [],
                },
            )
            event["tickets"].append(
                {
                    "id": row["ticket_id"],
                    "name": row["ticket_name"],
                    "price": row["price"],
                    "available": row["available"],
                }
            )
        return list(grouped.values())

    def ticket(self, ticket_id):
        with transaction() as cursor:
            cursor.execute(
                "SELECT id, name, price FROM ticket_types WHERE id = %s",
                (ticket_id,),
            )
            return cursor.fetchone()
