from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.view_decorators import LocationType
from flask_security import Security, SQLAlchemyUserDatastore, login_user
from sqlalchemy.exc import NoResultFound

from api.v1.users.models import UserM, RoleM
from database import db
from app import app
from errors import WasNotFoundError

user_datastore = SQLAlchemyUserDatastore(db, UserM, RoleM)
security = Security(app, user_datastore)


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
            try:
                user = db.session.get_one(UserM, user_id)
                login_user(user)
                return fn(*args, **kwargs)

            except NoResultFound:
                raise WasNotFoundError('User')

        return decorator

    return wrapper
