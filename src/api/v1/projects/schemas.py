from datetime import date

from pydantic import BaseModel, NonNegativeInt, Field, EmailStr

from base_pydantic_types import UTCDatetime, StrFrom3To255, Str500, StrTaskStatus
from global_schemas import PaginationQS


############################
# Схемы для модели проекта #
############################

class BaseProjectS(BaseModel):
    title:          StrFrom3To255
    description:    Str500 | None = None


class RequestBodyOfProjectS(BaseProjectS):
    ...


class ReadProjectS(RequestBodyOfProjectS):
    id:             NonNegativeInt
    created_at:     UTCDatetime
    updated_at:     UTCDatetime
    owner_id:       NonNegativeInt


class CreateProjectS(BaseProjectS):
    owner_id:       NonNegativeInt


class UpdateProjectS(BaseProjectS):
    ...


class ProjectPath(BaseModel):
    project_id: int

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


class ReadTaskWithMedia(ReadTaskS):
    media: list[str]


class CreateTaskS(RequestBodyOfTaskS):
    author_id:      NonNegativeInt


class CreateTaskFromEmailS(CreateTaskS):
    email_uid:      int
    email_author:   EmailStr


class UpdateTaskS(BaseModel):
    assignee_id:    NonNegativeInt | None = None
    status:         StrTaskStatus


class FilterTaskQS(PaginationQS):
    project_id:     NonNegativeInt | None = None
    status:         StrTaskStatus | None = None
    author_id:      NonNegativeInt | None = None
    assignee_id:    NonNegativeInt | None = None
    title:          str | None = None
    from_:          date | None = Field(default=None, alias='from')
    to:             date | None = None


class TaskPath(BaseModel):
    task_id: int

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


class CommentPath(BaseModel):
    comment_id: int
