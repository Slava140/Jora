from typing import Any

from flask import g
from sqlalchemy import insert, select, update
from sqlalchemy.orm.attributes import InstrumentedAttribute

from api.v1.users.models import UserM
from api.v1.users.schemas import CreateUserS, ReadUserS, BaseUserS, FullUserS
from security import get_hashed_password
from errors import AlreadyExistsError, WasNotFoundError
from database import db
from logger import get_logger

logger = get_logger('UserDAO')


class UserDAO:
    @staticmethod
    def _get_one_or_none(
            where: tuple[InstrumentedAttribute, Any],
            exclude_where: tuple[InstrumentedAttribute, Any] | None = None,
            is_active_state: bool | None = None
    ) -> UserM | None:
        """
        :param where: Первый элемент - поле модели. Второй элемент - значение которому поле должно быть равно.
        :param exclude_where: Аналогично where, но исключает поля.
        :param is_active_state: None, чтобы игнорировать состояние, True/False выбрать записи с указанным состоянием.
        """

        where_model_field, where_data = where
        where_conditions = [where_model_field == where_data]

        if exclude_where is not None:
            excluded_where_model_field, excluded_where_data = exclude_where
            where_conditions.append(
                excluded_where_model_field.not_in([excluded_where_data])
            )

        if is_active_state is not None:
            where_conditions.append(UserM.active.is_(is_active_state))

        query = select(UserM).where(*where_conditions).limit(1)

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
            password=get_hashed_password(user.password)
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
        query = select(
            UserM
        ).where(
            UserM.active.is_(True)
        ).limit(limit).offset((page - 1) * limit)
        result = db.session.execute(query).scalars().fetchall()
        return tuple(ReadUserS(**data.to_dict()) for data in result)

    @staticmethod
    def get_one_by_id_or_none(user_id: int) -> ReadUserS | None:
        query = select(
            UserM
        ).where(
            UserM.id == user_id,
            UserM.active.is_(True)
        )

        result = db.session.execute(query).scalar_one_or_none()

        return ReadUserS(**result.to_dict()) if result is not None else None

    @staticmethod
    def get_user_with_password_or_none(user_email: str) -> FullUserS | None:
        user = UserDAO._get_one_or_none(where=(UserM.email, user_email), is_active_state=True)
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

        with db.session.begin(nested=True) as transaction:
            user = UserDAO._get_one_or_none(where=(UserM.id, user_id), is_active_state=True)

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

            result = transaction.session.execute(stmt).mappings().one()

            # transaction.commit()

        return ReadUserS(**result)

    @staticmethod
    def delete_by_id(user_id: int) -> None:
        from api.v1.projects.dao import ProjectDAO
        stmt = update(
            UserM
        ).where(
            UserM.id == user_id
        ).values(
            active=False
        )

        transaction = db.session.begin(nested=True)
        transaction.session.execute(stmt)
        ProjectDAO.delete_all_projects_with_user_id(user_id, transaction)
        db.session.commit()

        return None
