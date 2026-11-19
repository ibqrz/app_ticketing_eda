from common.database import transaction


class SessionRepository:
    def add(self, token_hash, user_id, days):
        with transaction() as cursor:
            cursor.execute("DELETE FROM sessions WHERE expires_at < now()")
            cursor.execute(
                "INSERT INTO sessions (token_hash, user_id, expires_at) "
                "VALUES (%s, %s, now() + make_interval(days => %s))",
                (token_hash, user_id, days),
            )

    def user(self, token_hash):
        with transaction() as cursor:
            cursor.execute(
                "SELECT u.id, u.name, u.email, u.tickets FROM sessions s "
                "JOIN users u ON u.id = s.user_id "
                "WHERE s.token_hash = %s AND s.expires_at > now()",
                (token_hash,),
            )
            return cursor.fetchone()

    def remove(self, token_hash):
        with transaction() as cursor:
            cursor.execute("DELETE FROM sessions WHERE token_hash = %s", (token_hash,))
