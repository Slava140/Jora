from typing import Any

from sqlalchemy import insert, select, update
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import Session

from database import engine, get_db

from api.v1.users.models import UserM
from api.v1.users.schemas import CreateUserS, ReadUserS
from api.v1.auth.utils import get_hashed_password
from errors import AlreadyExistsError


class UserDAO:
    @staticmethod
    def is_exists(field: InstrumentedAttribute, value: Any, session: Session | None = None) -> bool:
        session = next(get_db()) if session is None else session
        query = select(1).where(field == value).limit(1)
        return session.execute(query).scalar_one_or_none() is not None

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
            if UserDAO.is_exists(UserM.email, user.email):
                raise AlreadyExistsError(f'UserM(email={user.email})')

            if UserDAO.is_exists(UserM.username, user.username):
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
    def update_by_id(user_id: int, updated_user: CreateUserS) -> ReadUserS:
        stmt = update(
            UserM
        ).where(
            UserM.id == user_id
        ).values(
            **updated_user.model_dump(exclude={'password'})
        ).returning(
            '*'
        )

        with next(get_db()) as session:
            if UserDAO.is_exists(UserM.email, updated_user.email):
                raise AlreadyExistsError(f'UserM(email={updated_user.email})')

            if UserDAO.is_exists(UserM.username, updated_user.username):
                raise AlreadyExistsError(f'UserM(username={updated_user.username})')

            result = session.execute(stmt).mappings().one_or_none()

        return ReadUserS(**result)
