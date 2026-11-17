from common.database import transaction

COLUMNS = (
    "id::text AS id, event_title, ticket_name, quantity, total, "
    "status, reason, processed_by, created_at"
)


class OrderRepository:
    def add(self, event):
        with transaction() as cursor:
            cursor.execute(
                "INSERT INTO orders "
                "(id, ticket_type_id, quantity, total, customer_name, customer_email) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    event.order_id,
                    event.ticket_type_id,
                    event.quantity,
                    event.total,
                    event.customer_name,
                    event.customer_email,
                ),
            )

    def remove(self, order_id):
        with transaction() as cursor:
            cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))

    def find(self, order_id):
        with transaction() as cursor:
            cursor.execute(
                f"SELECT {COLUMNS} FROM order_overview WHERE id = %s",
                (order_id,),
            )
            return cursor.fetchone()

    def recent(self, limit):
        with transaction() as cursor:
            cursor.execute(
                f"SELECT {COLUMNS} FROM order_overview "
                "ORDER BY created_at DESC LIMIT %s",
                (limit,),
            )
            return cursor.fetchall()

    def notifications(self, order_id):
        with transaction() as cursor:
            cursor.execute(
                "SELECT message FROM notifications WHERE order_id = %s ORDER BY id",
                (order_id,),
            )
            return [row["message"] for row in cursor.fetchall()]
