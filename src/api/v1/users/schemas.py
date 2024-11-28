from pydantic import BaseModel, NonNegativeInt, EmailStr, Field
from base_pydantic_types import StrFrom3To255, UTCDatetime, PasswordStr


class BaseUserS(BaseModel):
    username:           StrFrom3To255
    email:              EmailStr


class CreateUserS(BaseUserS):
    password:    PasswordStr


class ReadUserS(BaseUserS):
    id:                 NonNegativeInt
    created_at:         UTCDatetime
    updated_at:         UTCDatetime
