from pydantic import BaseModel, NonNegativeInt

from base_pydantic_types import UTCDatetime, StrFrom3To255, Str500, StrTaskStatus


############################
# Схемы для модели проекта #
############################

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


###########################
# Схемы для модели задачи #
###########################

class BaseTaskS(BaseModel):
    title:          StrFrom3To255
    description:    str
    status:         StrTaskStatus
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


class UpdateTaskS(BaseModel):
    assignee_id:    NonNegativeInt | None = None
    status:         StrTaskStatus


################################
# Схемы для модели комментария #
################################

class BaseCommentS(BaseModel):
    content:        str
    task_id:        NonNegativeInt


class RequestBodyOfCommentS(BaseCommentS):
    ...


class CreateCommentS(RequestBodyOfCommentS):
    author_id:      NonNegativeInt


class ReadCommentS(BaseCommentS):
    id:             NonNegativeInt
    created_at:     UTCDatetime
    author_id:      NonNegativeInt
