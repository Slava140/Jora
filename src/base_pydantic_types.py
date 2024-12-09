import re
from datetime import datetime, timezone
from typing import Annotated

from pydantic import Field, AfterValidator


def is_utc_datetime_validator(value: datetime) -> datetime:
    tz = value.tzinfo
    if tz is timezone.utc:
        return value
    else:
        raise ValueError('datetime must have a UTC timezone.')


def password_validator(value: str) -> str:
    if len(value) < 8:
        raise ValueError('Password length must be greater or equal than 8')

    if len(value) > 20:
        raise ValueError('Password length must be less or equal than 20')

    if not re.search(r'\d', value):
        raise ValueError('Password must contain at least one digit')

    if not re.search(r'[A-Z]', value):
        raise ValueError('Password must contain at least one uppercase letter')

    if not re.search(r'[a-z]', value):
        raise ValueError('Password must contain at least one lowercase letter')

    return value


StrFrom3To255 = Annotated[str, Field(min_length=3, max_length=255)]
Str500 = Annotated[str, Field(max_length=500)]

UTCDatetime = Annotated[datetime, AfterValidator(is_utc_datetime_validator)]
PasswordStr = Annotated[str, AfterValidator(password_validator)]
