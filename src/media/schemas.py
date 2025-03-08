from pathlib import Path

from flask_openapi3 import FileStorage
from pydantic import BaseModel, NonNegativeInt

from base_pydantic_types import UTCDatetime, StrFileWithExtension


class UploadMediaS(BaseModel):
    file:        FileStorage
    compress_it: bool
    task_id:     NonNegativeInt


class MediaMetadataS(BaseModel):
    task_id:   NonNegativeInt
    author_id: NonNegativeInt


class BaseMediaS(MediaMetadataS):
    filename: StrFileWithExtension


class CreateMediaS(BaseMediaS):
    ...

class ReadMediaS(BaseMediaS):
    id:         NonNegativeInt
    created_at: UTCDatetime


class ReadMediaWithFilepathS(ReadMediaS):
    filepath:   Path


class MediaPath(BaseModel):
    media_id: NonNegativeInt