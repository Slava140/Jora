from pydantic import BaseModel, NonNegativeInt, EmailStr, Field
from base_pydantic_types import StrFrom3To255, UTCDatetime, PasswordStr


class BaseUserS(BaseModel):
    id:                 NonNegativeInt | None = None
    username:           StrFrom3To255
    email:              EmailStr
    created_at:         UTCDatetime | None = None
    updated_at:         UTCDatetime | None = None


class UserWithPlainPassS(BaseUserS):
    password:           PasswordStr
