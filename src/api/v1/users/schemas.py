from pydantic import BaseModel, NonNegativeInt, PositiveInt, EmailStr
from base_pydantic_types import StrFrom3To255, UTCDatetime, PasswordStr


class BaseUserS(BaseModel):
    username:       StrFrom3To255
    email:          EmailStr


class CreateUserS(BaseUserS):
    password:       PasswordStr


class ReadUserS(BaseUserS):
    id:             NonNegativeInt
    created_at:     UTCDatetime
    updated_at:     UTCDatetime


class PaginationQS(BaseModel):
    page:           PositiveInt = 1
    limit:          PositiveInt = 10
