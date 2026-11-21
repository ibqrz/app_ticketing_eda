from fastapi import APIRouter, Depends

from container import auth_service
from controllers.dependencies import bearer
from schemas.auth import AuthResponse, LoginRequest, RegisterRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(data: RegisterRequest):
    return auth_service.register(data)


@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest):
    return auth_service.login(data)


@router.post("/logout", status_code=204)
def logout(token: str = Depends(bearer)):
    auth_service.logout(token)