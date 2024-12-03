from pydantic import BaseModel, NonNegativeInt

from base_pydantic_types import UTCDatetime, StrFrom3To255, Str500


class BaseProjectS(BaseModel):
    title: StrFrom3To255
    description: Str500 | None = None
    owner_id: NonNegativeInt


class ReadProjectS(BaseProjectS):
    id: NonNegativeInt
    created_at:     UTCDatetime
    updated_at:     UTCDatetime


class CreateProjectS(BaseProjectS):
    ...
