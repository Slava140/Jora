import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, AfterValidator, BeforeValidator, BaseModel, PlainSerializer

from api.v1.projects.models import Status
from config import settings
from errors import ExtensionsNotAllowedError


def is_utc_datetime_validator(value: datetime) -> datetime:
    if isinstance(value, str):
        return datetime.strptime(value, '%d.%m.%Y %X%z').astimezone(timezone.utc)
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    else:
        raise ValueError('Value must be datetime.')


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


def extension_validator(value: str) -> str:
    file_path = Path(value)
    extension = file_path.suffix.strip('.')
    if extension not in settings.allowed_file_extensions:
        raise ExtensionsNotAllowedError(extension)
    return file_path.name


def datetime_serializer(value: datetime) -> str:
    if isinstance(value, datetime):
        return value.strftime('%d.%m.%Y %X%z')


StrFrom3To255 = Annotated[str, Field(min_length=3, max_length=255)]
Str500 = Annotated[str, Field(max_length=500)]

StrTaskStatus = Annotated[Literal['open', 'in_progress', 'finished'], Field(default=Status.open)]

UTCDatetime = Annotated[
    datetime,
    BeforeValidator(is_utc_datetime_validator),
    PlainSerializer(datetime_serializer, return_type=str, when_used='json')
]
PasswordStr = Annotated[str, AfterValidator(password_validator)]
StrFileWithExtension = Annotated[str, AfterValidator(extension_validator)]
