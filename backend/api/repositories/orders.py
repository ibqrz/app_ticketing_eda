from common.database import transaction

COLUMNS = (
    "id::text AS id, ticket_id, ticket_name, ticket_type, quantity, total, "
    "location, organizer, description, image, dt_event, active, status, stage, reason, "
    "processed_by, refunded, created_at"
)

SCOPES = {
    "purchased": "status = 'CONFIRMED'",
    "tracking": "status IN ('PROCESSING', 'REFUSED')",
}


class OrderRepository:
    def add(self, event):
        with transaction() as cursor:
            cursor.execute(
                "INSERT INTO orders (id, user_id, ticket_id, ticket_type, quantity, total) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    event.order_id,
                    event.user_id,
                    event.ticket_id,
                    event.ticket_type,
                    event.quantity,
                    event.total,
                ),
            )

    def remove(self, order_id):
        with transaction() as cursor:
            cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))

    def find(self, order_id, user_id):
        with transaction() as cursor:
            cursor.execute(
                f"SELECT {COLUMNS} FROM order_overview WHERE id = %s AND user_id = %s",
                (order_id, user_id),
            )
            return cursor.fetchone()

    def recent(self, user_id, scope, limit):
        with transaction() as cursor:
            cursor.execute(
                f"SELECT {COLUMNS} FROM order_overview "
                f"WHERE user_id = %s AND {SCOPES[scope]} "
                "ORDER BY created_at DESC LIMIT %s",
                (user_id, limit),
            )
            return cursor.fetchall()

    def notifications(self, order_id):
        with transaction() as cursor:
            cursor.execute(
                "SELECT message FROM notifications WHERE order_id = %s ORDER BY id",
                (order_id,),
            )
            return [row["message"] for row in cursor.fetchall()]
