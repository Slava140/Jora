from api.v1.users.dao import UserDAO
from api.v1.users.schemas import CreateUserS, ReadUserS
from errors import AlreadyExistsError


class UserService:
    @staticmethod
    def add(user: CreateUserS) -> ReadUserS:
        return UserDAO.add(user)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadUserS, ...]:
        """
        :except ValueError
        """
        if limit <= 0 or page <= 0:
            raise ValueError('limit and page must be positive.')
        return UserDAO.get_many(limit, page)

    @staticmethod
    def get_one_by_id_or_none(user_id: int) -> ReadUserS:
        return UserDAO.get_one_by_id_or_none(user_id)
