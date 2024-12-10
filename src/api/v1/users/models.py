from sqlalchemy.orm import Mapped

from database import Base, pk_int, str_255_unique, created_at, updated_at, is_active


class UserM(Base):
    __tablename__ = 'users'

    id:                 Mapped[pk_int]
    username:           Mapped[str_255_unique]
    email:              Mapped[str_255_unique]
    hashed_password:    Mapped[str]
    is_active:          Mapped[is_active]
    created_at:         Mapped[created_at]
    updated_at:         Mapped[updated_at]
