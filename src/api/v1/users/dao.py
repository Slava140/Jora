from typing import Any, Self

from sqlalchemy import insert, select, update, and_, delete
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import Session

from database import engine, get_db

from api.v1.users.models import UserM
from api.v1.users.schemas import CreateUserS, ReadUserS, BaseUserS
from api.v1.auth.utils import get_hashed_password
from errors import AlreadyExistsError, WasNotFoundError


class UserDAO:
    # @staticmethod
    # def is_exists(field: InstrumentedAttribute, value: Any, session: Session | None = None) -> bool:
    #     return get_db()

    @staticmethod
    def get_by(
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
            if UserDAO.get_by((UserM.email, user.email), session=session) is not None:
                raise AlreadyExistsError(f'UserM(email={user.email})')

            if UserDAO.get_by((UserM.username, user.username), session=session) is not None:
                raise AlreadyExistsError(f'UserM(username={user.username})')

            result = session.execute(stmt).mappings().one_or_none()
            session.commit()

        return ReadUserS(**result)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadUserS, ...]:
        query = select(UserM).limit(limit).offset((page - 1) * limit)
        with next(get_db()) as session:
            result = session.execute(query).scalars().fetchall()
        return tuple(ReadUserS(**data.__dict__) for data in result)

    @staticmethod
    def get_one_by_id_or_none(user_id: int) -> ReadUserS | None:
        query = select(
            UserM
        ).where(
            UserM.id == user_id
        )

        with engine.connect() as session:
            result = session.execute(query).mappings().one_or_none()

        return ReadUserS(**result) if result is not None else None

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
        ).returning(
            '*'
        )

        with next(get_db()) as session:
            user = UserDAO.get_by(where=(UserM.id, user_id), session=session)

            if user is None:
                raise WasNotFoundError(f'UserM(id={user_id})')

            if user.email == updated_user.email and user.username == updated_user.username:
                return ReadUserS(**user.to_dict())

            is_email_unique = UserDAO.get_by(
                where=(UserM.email, updated_user.email), exclude_where=(UserM.id, user_id), session=session
            ) is None
            if not is_email_unique:
                raise AlreadyExistsError(f'UserM(email={updated_user.email})')

            is_username_unique = UserDAO.get_by(
                where=(UserM.username, updated_user.username), exclude_where=(UserM.id, user_id), session=session
            ) is None
            if not is_username_unique:
                raise AlreadyExistsError(f'UserM(username={updated_user.username})')

            result = session.execute(stmt).mappings().one_or_none()
            session.commit()

        return ReadUserS(**result)

    @staticmethod
    def delete_by_id(user_id: int) -> None:
        stmt = delete(UserM).where(UserM.id == user_id)
        with next(get_db()) as session:
            session.execute(stmt)
            session.commit()

        return None
