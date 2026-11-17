from common.database import transaction


class PaymentRepository:
    def save(self, order_id, amount, status, reason, processed_by):
        with transaction() as cursor:
            cursor.execute(
                "INSERT INTO payments (order_id, amount, status, reason, processed_by) "
                "VALUES (%s, %s, %s, %s, %s) ON CONFLICT (order_id) DO NOTHING",
                (order_id, amount, status, reason, processed_by),
            )
