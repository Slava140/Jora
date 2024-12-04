from typing import Any

from sqlalchemy import insert, select, update, and_, delete
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import Session

from database import get_db

from api.v1.users.models import UserM
from api.v1.users.schemas import CreateUserS, ReadUserS, BaseUserS, FullUserS
from api.v1.users.utils import get_hashed_password
from errors import AlreadyExistsError, WasNotFoundError


class UserDAO:
    # @staticmethod
    # def is_exists(field: InstrumentedAttribute, value: Any, session: Session | None = None) -> bool:
    #     return get_db()

    @staticmethod
    def _get_one_or_none(
            where: tuple[InstrumentedAttribute, Any],
            exclude_where: tuple[InstrumentedAttribute, Any] | None = None,
            session: Session | None = None) -> UserM | None:

        session = next(get_db()) if session is None else session
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
        return session.execute(query).scalar_one_or_none()

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

        with next(get_db()) as session:
            if UserDAO._get_one_or_none((UserM.email, user.email), session=session) is not None:
                raise AlreadyExistsError(f'UserM(email={user.email})')

            if UserDAO._get_one_or_none((UserM.username, user.username), session=session) is not None:
                raise AlreadyExistsError(f'UserM(username={user.username})')

            result = session.execute(stmt).mappings().one()
            session.commit()

        return ReadUserS(**result)

    @staticmethod
    def get_many(limit: int, page: int) -> list[ReadUserS]:
        query = select(UserM).limit(limit).offset((page - 1) * limit)
        with next(get_db()) as session:
            result = session.execute(query).scalars().fetchall()
        return [ReadUserS(**data.to_dict()) for data in result]

    @staticmethod
    def get_one_by_id_or_none(user_id: int) -> ReadUserS | None:
        query = select(
            UserM
        ).where(
            UserM.id == user_id
        )

        with next(get_db()) as session:
            result = session.execute(query).scalar_one_or_none()

        return ReadUserS(**result.to_dict()) if result is not None else None

    @staticmethod
    def get_one_by_email_or_none(user_email: str) -> ReadUserS | None:
        user = UserDAO._get_one_or_none(where=(UserM.email == user_email))
        return ReadUserS(**user.to_dict()) if user is not None else None

    @staticmethod
    def get_user_with_password(user_email: str) -> FullUserS:
        user = UserDAO._get_one_or_none(where=(UserM.email == user_email))
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

        with next(get_db()) as session:
            user = UserDAO._get_one_or_none(where=(UserM.id, user_id), session=session)

            if user is None:
                raise WasNotFoundError(f'UserM(id={user_id})')

            is_email_unique = UserDAO._get_one_or_none(
                where=(UserM.email, updated_user.email), exclude_where=(UserM.id, user_id), session=session
            ) is None
            if not is_email_unique:
                raise AlreadyExistsError(f'UserM(email={updated_user.email})')

            is_username_unique = UserDAO._get_one_or_none(
                where=(UserM.username, updated_user.username), exclude_where=(UserM.id, user_id), session=session
            ) is None
            if not is_username_unique:
                raise AlreadyExistsError(f'UserM(username={updated_user.username})')

            result = session.execute(stmt).mappings().one()
            session.commit()

        return ReadUserS(**result)

    @staticmethod
    def delete_by_id(user_id: int) -> None:
        stmt = delete(UserM).where(UserM.id == user_id)

        with next(get_db()) as session:
            session.execute(stmt)
            session.commit()

        return None
