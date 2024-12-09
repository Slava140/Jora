from pydantic import BaseModel, NonNegativeInt, EmailStr
from base_pydantic_types import StrFrom3To255, UTCDatetime, PasswordStr


class BaseUserS(BaseModel):
    username:   StrFrom3To255
    email:      EmailStr


class CreateUserS(BaseUserS):
    password:   PasswordStr


class ReadUserS(BaseUserS):
    id:             NonNegativeInt
    created_at:     UTCDatetime
    updated_at:     UTCDatetime


class FullUserS(ReadUserS):
    hashed_password:    str


# class AccessTokenPayloadS(BaseModel):
#     sub:    NonNegativeInt
#     exp:    NonNegativeInt


class LoginS(BaseModel):
    email:      EmailStr
    password:   str


class LoggedInS(ReadUserS):
    access_token:   str
