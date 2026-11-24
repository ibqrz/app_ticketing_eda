import json

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

    def refund(self, event):
        with transaction() as cursor:
            cursor.execute(
                "SELECT user_id, ticket_id, quantity FROM orders WHERE id = %s FOR UPDATE",
                (event.order_id,),
            )
            order = cursor.fetchone()
            cursor.execute("SELECT 1 FROM refunds WHERE id = %s", (event.refund_id,))
            if cursor.fetchone():
                return "DUPLICATE"
            if order is None or not self.refundable(cursor, event, order):
                return "DENIED"
            cursor.execute(
                "SELECT tickets FROM users WHERE id = %s FOR UPDATE", (event.user_id,)
            )
            owned = cursor.fetchone()["tickets"]
            if event.ticket_id not in owned:
                return "DENIED"
            owned.remove(event.ticket_id)
            cursor.execute(
                "UPDATE users SET tickets = %s::jsonb WHERE id = %s",
                (json.dumps(owned), event.user_id),
            )
            cursor.execute(
                "INSERT INTO refunds (id, order_id, user_id, ticket_id) "
                "VALUES (%s, %s, %s, %s)",
                (event.refund_id, event.order_id, event.user_id, event.ticket_id),
            )
            cursor.execute(
                "UPDATE tickets SET available = available + 1, "
                "info = info - 'dtFinished' WHERE id = %s",
                (event.ticket_id,),
            )
            return "DONE"

    def refundable(self, cursor, event, order):
        if order["user_id"] != event.user_id or order["ticket_id"] != event.ticket_id:
            return False
        cursor.execute(
            "SELECT r.status, (t.info ->> 'dtEvent')::timestamptz > now() AS active, "
            "(SELECT count(*) FROM refunds WHERE order_id = %(order)s) AS refunded "
            "FROM stock_reservations r JOIN tickets t ON t.id = r.ticket_id "
            "WHERE r.order_id = %(order)s",
            {"order": event.order_id},
        )
        row = cursor.fetchone()
        return (
            row is not None
            and row["status"] == "CONFIRMED"
            and row["active"]
            and row["refunded"] < order["quantity"]
        )