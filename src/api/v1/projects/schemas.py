from typing import Literal

from pydantic import BaseModel, NonNegativeInt

from base_pydantic_types import UTCDatetime, StrFrom3To255, Str500, StrTaskStatus


class BaseProjectS(BaseModel):
    title:          StrFrom3To255
    description:    Str500 | None = None
    owner_id:       NonNegativeInt


class ReadProjectS(BaseProjectS):
    id:             NonNegativeInt
    created_at:     UTCDatetime
    updated_at:     UTCDatetime


class CreateProjectS(BaseProjectS):
    ...


class BaseTaskS(BaseModel):
    title:          StrFrom3To255
    description:    str
    status:         Literal['open', 'in_progress', 'finished'] = 'open'
    due_date:       UTCDatetime | None = None
    project_id:     NonNegativeInt


class RequestBodyOfTaskS(BaseTaskS):
    ...


class ReadTaskS(BaseTaskS):
    id:             NonNegativeInt
    finished_at:    UTCDatetime | None = None
    created_at:     UTCDatetime
    updated_at:     UTCDatetime
    assignee_id:    NonNegativeInt | None = None
    author_id:      NonNegativeInt


class CreateTaskS(RequestBodyOfTaskS):
    author_id:      NonNegativeInt
