from common.database import transaction


class TicketRepository:
    def all(self):
        with transaction() as cursor:
            cursor.execute(
                "SELECT id, info, image, available FROM tickets "
                "ORDER BY (info ->> 'dtEvent')::timestamptz, id"
            )
            return cursor.fetchall()

    def find(self, ticket_id):
        with transaction() as cursor:
            cursor.execute(
                "SELECT id, info, image, available FROM tickets WHERE id = %s",
                (ticket_id,),
            )
            return cursor.fetchone()
