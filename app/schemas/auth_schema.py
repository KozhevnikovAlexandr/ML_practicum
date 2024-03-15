
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    email: str


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserRegisterSchema(BaseModel):
    name: str
    email: str
    password: str


class UserLoginResponseSchema(BaseModel):
    access_token: str
    user_info: UserSchema


class BalanceSchema(BaseModel):
    balance: int