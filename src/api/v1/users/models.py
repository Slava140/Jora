from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import Mapped

from database import Base, pk_int, str_255_unique, created_at, updated_at, is_active, fk_user_id, fk_role_id


class RoleM(Base, RoleMixin):
    __tablename__ = 'roles'

    id:     Mapped[pk_int]
    name:   Mapped[str_255_unique]


class UserM(Base, UserMixin):
    __tablename__ = 'users'

    id:                 Mapped[pk_int]
    username:           Mapped[str_255_unique]
    email:              Mapped[str_255_unique]
    hashed_password:    Mapped[str]
    is_active:          Mapped[is_active]
    created_at:         Mapped[created_at]
    updated_at:         Mapped[updated_at]


class RoleUserM(Base):
    __tablename__ = 'roles_users'

    id:         Mapped[pk_int]
    user_id:    Mapped[fk_user_id]
    role_id:    Mapped[fk_role_id]