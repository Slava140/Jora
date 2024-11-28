from pydantic import BaseModel, NonNegativeInt, EmailStr
from base_pydantic_types import StrFrom3To255, UTCDatetime, PasswordStr


class UserS(BaseModel):
    id:                 NonNegativeInt
    username:           StrFrom3To255
    email:              EmailStr
    hashed_password:    str
    created_at:         UTCDatetime
    updated_at:         UTCDatetime