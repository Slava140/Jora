from flask_security.models import fsqla
from sqlalchemy.orm import Mapped

from database import db, Base, pk_int, str_255_unique, created_at, updated_at, is_active

fsqla.FsModels.set_db_info(db, user_table_name='users', role_table_name='roles')

class RoleM(Base, fsqla.FsRoleMixin):
    __tablename__ = 'roles'


class UserM(Base, fsqla.UserMixin):
    __tablename__ = 'users'

    id:                 Mapped[pk_int]
    username:           Mapped[str_255_unique]
    email:              Mapped[str_255_unique]
    password:           Mapped[str]
    active:             Mapped[is_active]
    create_datetime:    Mapped[created_at]
    update_datetime:    Mapped[updated_at]
    fs_uniquifier:      Mapped[str_255_unique]

    roles = db.relationship('RoleM', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
