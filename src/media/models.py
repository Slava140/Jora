from sqlalchemy.orm import Mapped

from database import Base, pk_int, str_255, str_500, created_at, is_archived, fk_task_id, fk_user_id


class MediaM(Base):
    __tablename__ = 'media'

    id:             Mapped[pk_int]
    filename:       Mapped[str_500]
    extension:      Mapped[str_255]
    created_at:     Mapped[created_at]
    is_archived:    Mapped[is_archived]

    task_id:        Mapped[fk_task_id]
    author_id:      Mapped[fk_user_id]
