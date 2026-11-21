from common.config import settings
from common.errors import ConflictError, UnauthorizedError
from security import hash_password, hash_token, new_token, verify_password


def public(user):
    return {key: user[key] for key in ("id", "name", "email", "tickets")}


class AuthService:
    def __init__(self, users, sessions):
        self.users = users
        self.sessions = sessions

    def register(self, data):
        email = data.email.lower()
        if self.users.by_email(email):
            raise ConflictError("Este e-mail já está cadastrado.")
        user = self.users.add(data.name.strip(), email, hash_password(data.password))
        return self.open(user)

    def login(self, data):
        user = self.users.by_email(data.email.lower())
        if user is None or not verify_password(data.password, user["password"]):
            raise UnauthorizedError("E-mail ou senha inválidos.")
        return self.open(user)

    def open(self, user):
        token = new_token()
        self.sessions.add(hash_token(token), user["id"], settings.session_days)
        return {"token": token, "user": public(user)}

    def logout(self, token):
        self.sessions.remove(hash_token(token))

    def authenticate(self, token):
        user = self.sessions.user(hash_token(token))
        if user is None:
            raise UnauthorizedError("Sessão inválida ou expirada.")
        return user