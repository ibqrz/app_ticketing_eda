from common.database import transaction


class InventoryRepository:
    def reserve(self, order_id, ticket_id, quantity):
        with transaction() as cursor:
            cursor.execute(
                "SELECT status FROM stock_reservations WHERE order_id = %s",
                (order_id,),
            )
            row = cursor.fetchone()
            if row:
                return row["status"]
            cursor.execute(
                "UPDATE tickets SET available = available - %(quantity)s, "
                "info = CASE WHEN available - %(quantity)s = 0 "
                "THEN jsonb_set(info, '{dtFinished}', to_jsonb(now())) "
                "ELSE info END "
                "WHERE id = %(ticket_id)s AND available >= %(quantity)s",
                {"quantity": quantity, "ticket_id": ticket_id},
            )
            status = "RESERVED" if cursor.rowcount == 1 else "SOLD_OUT"
            cursor.execute(
                "INSERT INTO stock_reservations (order_id, ticket_id, quantity, status) "
                "VALUES (%s, %s, %s, %s)",
                (order_id, ticket_id, quantity, status),
            )
            return status

    def confirm(self, order_id, user_id, ticket_id, quantity):
        with transaction() as cursor:
            cursor.execute(
                "UPDATE stock_reservations SET status = 'CONFIRMED', updated_at = now() "
                "WHERE order_id = %s AND status = 'RESERVED' RETURNING order_id",
                (order_id,),
            )
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE users SET tickets = tickets || COALESCE("
                    "(SELECT jsonb_agg(%s) FROM generate_series(1, %s)), '[]'::jsonb) "
                    "WHERE id = %s",
                    (ticket_id, quantity, user_id),
                )

    def release(self, order_id):
        with transaction() as cursor:
            cursor.execute(
                "UPDATE stock_reservations SET status = 'RELEASED', updated_at = now() "
                "WHERE order_id = %s AND status = 'RESERVED' "
                "RETURNING ticket_id, quantity",
                (order_id,),
            )
            row = cursor.fetchone()
            if row:
                cursor.execute(
                    "UPDATE tickets SET available = available + %s, "
                    "info = info - 'dtFinished' WHERE id = %s",
                    (row["quantity"], row["ticket_id"]),
                )
