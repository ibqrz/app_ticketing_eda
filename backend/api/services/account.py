from common.errors import BadRequestError
from security import hash_password, verify_password


class AccountService:
    def __init__(self, users):
        self.users = users

    def update(self, user, data):
        name = data.name.strip() if data.name else None
        email = data.email.lower() if data.email else None
        if name is None and email is None:
            raise BadRequestError("Informe o nome ou o e-mail para atualizar.")
        return self.users.update(user["id"], name, email)

    def change_password(self, user, data):
        row = self.users.find(user["id"])
        if not verify_password(data.current_password, row["password"]):
            raise BadRequestError("A senha atual está incorreta.")
        self.users.set_password(user["id"], hash_password(data.new_password))
