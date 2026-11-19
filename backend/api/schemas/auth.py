from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserView(BaseModel):
    id: int
    name: str
    email: str
    tickets: list[int] = []


class AuthResponse(BaseModel):
    token: str
    user: UserView
