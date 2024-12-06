from datetime import datetime, timezone

from api.v1.users.dao import UserDAO
from api.v1.users.schemas import CreateUserS, ReadUserS, BaseUserS, LoginS, LoggedInS, AccessTokenPayloadS
from api.v1.users.utils import is_correct_password, create_access_token
from config import settings
from errors import InvalidEmailOrPasswordError


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
    def get_one_by_id_or_none(user_id: int) -> ReadUserS | None:
        return UserDAO.get_one_by_id_or_none(user_id)

    @staticmethod
    def get_one_by_email_or_none(user_email: str) -> ReadUserS | None:
        return UserDAO.get_one_by_email_or_none(user_email)

    @staticmethod
    def login(data: LoginS) -> LoggedInS:
        """
        :except InvalidEmailOrPasswordError
        """
        user = UserDAO.get_user_with_password(data.email)
        if user is not None and is_correct_password(data.password, user.hashed_password):
            expires_in = datetime.now(tz=timezone.utc) + settings.access_token_ttl_timedelta
            exp = int(expires_in.timestamp())
            payload = AccessTokenPayloadS(sub=user.id, exp=exp)
            access_token = create_access_token(payload)
            return LoggedInS(**user.model_dump(), access_token=access_token, exp=exp)
        else:
            raise InvalidEmailOrPasswordError()

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
