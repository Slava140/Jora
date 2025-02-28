from functools import wraps

import bcrypt
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.view_decorators import LocationType
from flask_security import Security, SQLAlchemyUserDatastore, login_user

from api.v1.users.models import UserM, RoleM
from database import db
from app import app
from errors import ForbiddenError


def get_hashed_password(plain_password: str) -> str:
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=password_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def is_correct_password(plain: str, hashed: str) -> bool:
    password_bytes = plain.encode('utf-8')
    hashed_password_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


user_datastore = SQLAlchemyUserDatastore(db, UserM, RoleM)
security = Security(app, user_datastore)

with app.app_context():
    security.datastore.find_or_create_role(
        name='admin',
        description='admin role',
        permissions={'user-read', 'user-write',
                     'project-read', 'project-write',
                     'task-read', 'task-write'}
    )
    security.datastore.find_or_create_role(
        name='user',
        description='user role',
        permissions={'user-read',
                     'project-read',
                     'task-read', 'task-write'}
    )
    security.datastore.commit()


def jwt_required(
        optional: bool = False,
        fresh: bool = False,
        refresh: bool = False,
        locations: LocationType | None = None,
        verify_type: bool = True,
        skip_revocation_check: bool = False,
):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):

            verify_jwt_in_request(
                optional, fresh, refresh, locations, verify_type, skip_revocation_check
            )
            user_id = int(get_jwt_identity())
            user = security.datastore.find_user(id=user_id)
            if user is None:
                raise ForbiddenError()
            login_user(user)

            return fn(*args, **kwargs)
        return decorator
    return wrapper
