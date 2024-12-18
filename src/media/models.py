from sqlalchemy.orm import Mapped

from database import Base, pk_int, str_500, created_at, fk_task_id, fk_user_id


class MediaM(Base):
    __tablename__ = 'media'

    id:         Mapped[pk_int]
    filename:   Mapped[str_500]
    created_at: Mapped[created_at]

    task_id:    Mapped[fk_task_id]
    author_id:  Mapped[fk_user_id]
