from fastapi import APIRouter, Depends

from container import account_service
from controllers.dependencies import current_user
from schemas.account import PasswordChange, ProfileUpdate
from schemas.auth import UserView

router = APIRouter(prefix="/api/account", tags=["account"])


@router.get("", response_model=UserView)
def find(user=Depends(current_user)):
    return user


@router.patch("", response_model=UserView)
def update(data: ProfileUpdate, user=Depends(current_user)):
    return account_service.update(user, data)


@router.put("/password", status_code=204)
def change_password(data: PasswordChange, user=Depends(current_user)):
    account_service.change_password(user, data)