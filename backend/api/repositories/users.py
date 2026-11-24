from psycopg2.errors import UniqueViolation

from common.database import transaction
from common.errors import ConflictError

PUBLIC = "id, name, email, tickets"


class UserRepository:
    def add(self, name, email, password):
        try:
            with transaction() as cursor:
                cursor.execute(
                    f"INSERT INTO users (name, email, password) VALUES (%s, %s, %s) "
                    f"RETURNING {PUBLIC}",
                    (name, email, password),
                )
                return cursor.fetchone()
        except UniqueViolation as error:
            raise ConflictError("Este e-mail já está cadastrado.") from error

    def find(self, user_id):
        with transaction() as cursor:
            cursor.execute(
                f"SELECT {PUBLIC}, password FROM users WHERE id = %s", (user_id,)
            )
            return cursor.fetchone()

    def by_email(self, email):
        with transaction() as cursor:
            cursor.execute(
                f"SELECT {PUBLIC}, password FROM users WHERE email = %s", (email,)
            )
            return cursor.fetchone()

    def update(self, user_id, name, email):
        try:
            with transaction() as cursor:
                cursor.execute(
                    "UPDATE users SET name = COALESCE(%s, name), "
                    f"email = COALESCE(%s, email) WHERE id = %s RETURNING {PUBLIC}",
                    (name, email, user_id),
                )
                return cursor.fetchone()
        except UniqueViolation as error:
            raise ConflictError("Este e-mail já está cadastrado.") from error

    def set_password(self, user_id, password):
        with transaction() as cursor:
            cursor.execute(
                "UPDATE users SET password = %s WHERE id = %s", (password, user_id)
            )