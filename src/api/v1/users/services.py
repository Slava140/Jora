from sqlalchemy.exc import DatabaseError
from psycopg.errors import UniqueViolation
from sqlalchemy.orm import Session

from api.v1.users.dao import UserDAO
from api.v1.users.schemas import CreateUserS, ReadUserS
from errors import AlreadyExistsError


class UserService:
    @staticmethod
    def add(user: CreateUserS) -> ReadUserS:
        return UserDAO.add(user)

    @staticmethod
    def get_many(limit: int, page: int):
        """
        :except ValueError
        """
        if limit <= 0 or page <= 0:
            raise ValueError('limit and page must be positive.')
        r = UserDAO.get_many(limit, page)
        return r
