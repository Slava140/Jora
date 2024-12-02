from api.v1.users.dao import UserDAO
from api.v1.users.schemas import CreateUserS, ReadUserS, BaseUserS
from errors import AlreadyExistsError


class UserService:
    @staticmethod
    def add(user: CreateUserS) -> ReadUserS:
        """
        :except AlreadyExistsError
        """
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

    @staticmethod
    def update_by_id(user_id: int, updated_user: BaseUserS) -> ReadUserS:
        """
        :except AlreadyExistsError
        :except WasNotFoundError
        """
        return UserDAO.update_by_id(user_id, updated_user)

    @staticmethod
    def delete_by_id(user_id: int) -> None:
        return UserDAO.delete_by_id(user_id)
