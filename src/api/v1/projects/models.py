import enum

from sqlalchemy.orm import Mapped, relationship

from database import (Base,
                      pk_int, fk_user_id, fk_project_id, fk_task_id,
                      str_255, str_500,
                      created_at, updated_at, datetime_utc_tz,
                      task_status as status, is_archived
                      )
from media.models import MediaM


class Status(str, enum.Enum):
    open = 'open'
    in_progress = 'in_progress'
    finished = 'finished'


class TaskM(Base):
    __tablename__ = 'tasks'

    id:             Mapped[pk_int]
    title:          Mapped[str_255]
    description:    Mapped[str]
    status:         Mapped[status]
    due_date:       Mapped[datetime_utc_tz | None]
    finished_at:    Mapped[datetime_utc_tz | None]
    created_at:     Mapped[created_at]
    updated_at:     Mapped[updated_at]
    is_archived:    Mapped[is_archived]

    project_id:     Mapped[fk_project_id]
    author_id:      Mapped[fk_user_id]
    assignee_id:    Mapped[fk_user_id | None]

    media:          Mapped[list[MediaM]] = relationship()


class ProjectM(Base):
    __tablename__ = 'projects'

    id:             Mapped[pk_int]
    title:          Mapped[str_255]
    description:    Mapped[str_500 | None]
    created_at:     Mapped[created_at]
    updated_at:     Mapped[updated_at]
    is_archived:    Mapped[is_archived]

    owner_id:       Mapped[fk_user_id]


class CommentM(Base):
    __tablename__ = 'comments'

    id:             Mapped[pk_int]
    content:        Mapped[str]
    created_at:     Mapped[created_at]
    is_archived:    Mapped[is_archived]

    author_id:      Mapped[fk_user_id]
    task_id:        Mapped[fk_task_id]
