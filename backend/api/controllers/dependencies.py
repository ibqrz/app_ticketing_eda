from typing import Optional

from fastapi import Depends, Header

from common.errors import UnauthorizedError
from container import auth_service


def bearer(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Faça login para continuar.")
    return authorization[7:].strip()


def current_user(token: str = Depends(bearer)):
    return auth_service.authenticate(token)
