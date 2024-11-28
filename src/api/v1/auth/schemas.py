from pydantic import BaseModel
from base_pydantic_types import StrFrom3To255, PasswordStr


class LoginS(BaseModel):
    username:   StrFrom3To255
    password:   PasswordStr

