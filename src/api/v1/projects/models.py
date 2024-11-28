import enum

from database import Base, pk_int, fk_user_id, str_255, created_at, updated_at

# description
# tasks - project
# регистрация
# смена пароля
# управление проектом
class Status(enum.Enum):
    assigned = 'assigned'
    in_progress = 'in_progress'
    done = 'done'


class ProjectM(Base):
    __tablename__ = 'projects'

    id:                 pk_int
    title:              str_255
    description:        str_255 | None
    created_at:         created_at
    updated_at:         updated_at

    owner_id:           fk_user_id


# class Task(Base):
#     __tablename__ = 'tasks'
#
#     id: pk_int
#     title: str_255
#     description: str
#
#     project_id: int