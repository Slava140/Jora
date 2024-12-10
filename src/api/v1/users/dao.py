from typing import Any

from sqlalchemy import insert, select, update, and_, delete
from sqlalchemy.orm.attributes import InstrumentedAttribute

from api.v1.users.models import UserM
from api.v1.users.schemas import CreateUserS, ReadUserS, BaseUserS, FullUserS
from api.v1.users.utils import get_hashed_password
from errors import AlreadyExistsError, WasNotFoundError
from database import db


class UserDAO:
    @staticmethod
    def _get_one_or_none(
            where: tuple[InstrumentedAttribute, Any],
            exclude_where: tuple[InstrumentedAttribute, Any] | None = None) -> UserM | None:

        if exclude_where is None:
            query = select(UserM).where(where[0] == where[1]).limit(1)
        else:
            query = select(
                UserM
            ).where(
                and_(
                    where[0] == where[1],
                    exclude_where[0].not_in([exclude_where[1]])
                )
            ).limit(1)
        return db.session.execute(query).scalar_one_or_none()

    @staticmethod
    def add(user: CreateUserS) -> ReadUserS:
        """
        :except AlreadyExistsError
        """
        stmt = insert(
            UserM
        ).values(
            email=user.email,
            username=user.username,
            hashed_password=get_hashed_password(user.password)
        ).returning('*')

        with db.session.begin() as transaction:
            if UserDAO._get_one_or_none((UserM.email, user.email)) is not None:
                raise AlreadyExistsError(f'User with email {user.email}')

            if UserDAO._get_one_or_none((UserM.username, user.username)) is not None:
                raise AlreadyExistsError(f'User with username {user.username}')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadUserS(**result)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadUserS, ...]:
        query = select(UserM).limit(limit).offset((page - 1) * limit)
        result = db.session.execute(query).scalars().fetchall()
        return tuple(ReadUserS(**data.to_dict()) for data in result)

    @staticmethod
    def get_one_by_id_or_none(user_id: int) -> ReadUserS | None:
        query = select(
            UserM
        ).where(
            UserM.id == user_id
        )

        result = db.session.execute(query).scalar_one_or_none()

        return ReadUserS(**result.to_dict()) if result is not None else None

    @staticmethod
    def get_one_by_email_or_none(user_email: str) -> ReadUserS | None:
        user = UserDAO._get_one_or_none(where=(UserM.email == user_email))
        return ReadUserS(**user.to_dict()) if user is not None else None

    @staticmethod
    def get_user_with_password(user_email: str) -> FullUserS:
        user = UserDAO._get_one_or_none(where=(UserM.email, user_email))
        return FullUserS(**user.to_dict()) if user is not None else None

    @staticmethod
    def update_by_id(user_id: int, updated_user: BaseUserS) -> ReadUserS:
        """
        :except AlreadyExistsError
        :except WasNotFoundError
        """
        stmt = update(
            UserM
        ).where(
            UserM.id == user_id
        ).values(
            **updated_user.model_dump()
        ).returning('*')

        with db.session.begin() as transaction:
            user = UserDAO._get_one_or_none(where=(UserM.id, user_id))

            if user is None:
                raise WasNotFoundError(f'User with id {user_id}')

            is_email_unique = UserDAO._get_one_or_none(
                where=(UserM.email, updated_user.email), exclude_where=(UserM.id, user_id)
            ) is None
            if not is_email_unique:
                raise AlreadyExistsError(f'User with email {updated_user.email}')

            is_username_unique = UserDAO._get_one_or_none(
                where=(UserM.username, updated_user.username), exclude_where=(UserM.id, user_id)
            ) is None
            if not is_username_unique:
                raise AlreadyExistsError(f'User with username {updated_user.username}')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadUserS(**result)

    @staticmethod
    def delete_by_id(user_id: int) -> None:
        stmt = update(
            UserM
        ).where(
            UserM.id == user_id
        ).values(
            is_active=False
        )

        db.session.execute(stmt)
        db.session.commit()

        return None
