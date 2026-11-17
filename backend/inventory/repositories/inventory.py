from common.database import transaction


class InventoryRepository:
    def reserve(self, order_id, ticket_type_id, quantity):
        with transaction() as cursor:
            cursor.execute(
                "SELECT status FROM stock_reservations WHERE order_id = %s",
                (order_id,),
            )
            row = cursor.fetchone()
            if row:
                return row["status"]
            cursor.execute(
                "UPDATE stock_items SET available = available - %s "
                "WHERE ticket_type_id = %s AND available >= %s",
                (quantity, ticket_type_id, quantity),
            )
            status = "RESERVED" if cursor.rowcount == 1 else "SOLD_OUT"
            cursor.execute(
                "INSERT INTO stock_reservations (order_id, ticket_type_id, quantity, status) "
                "VALUES (%s, %s, %s, %s)",
                (order_id, ticket_type_id, quantity, status),
            )
            return status

    def confirm(self, order_id):
        with transaction() as cursor:
            cursor.execute(
                "UPDATE stock_reservations SET status = 'CONFIRMED', updated_at = now() "
                "WHERE order_id = %s AND status = 'RESERVED'",
                (order_id,),
            )

    def release(self, order_id):
        with transaction() as cursor:
            cursor.execute(
                "UPDATE stock_reservations SET status = 'RELEASED', updated_at = now() "
                "WHERE order_id = %s AND status = 'RESERVED' "
                "RETURNING ticket_type_id, quantity",
                (order_id,),
            )
            row = cursor.fetchone()
            if row:
                cursor.execute(
                    "UPDATE stock_items SET available = available + %s "
                    "WHERE ticket_type_id = %s",
                    (row["quantity"], row["ticket_type_id"]),
                )
