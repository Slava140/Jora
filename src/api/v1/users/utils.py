import datetime

import bcrypt
import jwt

from api.v1.users.schemas import AccessTokenPayloadS
from config import settings


def get_hashed_password(plain_password: str) -> str:
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=password_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def is_correct_password(plain: str, hashed: str) -> bool:
    password_bytes = plain.encode('utf-8')
    hashed_password_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def create_access_token(payload: AccessTokenPayloadS):
    return jwt.encode(payload=payload.model_dump(), key=settings.JWT_SECRET, algorithm='HS256')
