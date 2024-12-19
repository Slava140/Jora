from pathlib import Path

from pydantic import BaseModel, NonNegativeInt

from base_pydantic_types import Str500, UTCDatetime


class MediaQS(BaseModel):
    task_id:    NonNegativeInt


class BaseMediaS(BaseModel):
    filename:   Str500
    task_id:    NonNegativeInt
    author_id:  NonNegativeInt


class CreateMediaS(BaseMediaS):
    ...


class ReadMediaS(BaseMediaS):
    id:         NonNegativeInt
    created_at: UTCDatetime


class ReadMediaWithFilepathS(ReadMediaS):
    filepath:   Path
