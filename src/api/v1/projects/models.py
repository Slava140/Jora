import enum

from sqlalchemy.orm import Mapped

from database import Base, pk_int, fk_user_id, str_255, created_at, updated_at, str_500


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

    id:                 Mapped[pk_int]
    title:              Mapped[str_255]
    description:        Mapped[str_500 | None]
    created_at:         Mapped[created_at]
    updated_at:         Mapped[updated_at]

    owner_id:           Mapped[fk_user_id]
