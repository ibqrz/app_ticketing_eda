from common.database import transaction


class NotificationRepository:
    def save(self, order_id, kind, message):
        with transaction() as cursor:
            cursor.execute(
                "INSERT INTO notifications (order_id, kind, message) "
                "VALUES (%s, %s, %s) ON CONFLICT (order_id, kind) DO NOTHING",
                (order_id, kind, message),
            )
