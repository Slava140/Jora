from sqlalchemy.exc import DatabaseError
from psycopg.errors import UniqueViolation
from sqlalchemy.orm import Session

from api.v1.users.dao import UserDAO
from api.v1.users.schemas import CreateUserS, ReadUserS
from errors import AlreadyExistsError


class UserService:
    @staticmethod
    def add(user: CreateUserS) -> ReadUserS:
        return UserDAO.insert(user)

