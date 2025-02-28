from flask_jwt_extended import create_access_token
from flask_security import logout_user

from api.v1.users.dao import UserDAO
from api.v1.users.schemas import CreateUserS, ReadUserS, BaseUserS, LoginS, LoggedInS
from errors import InvalidEmailOrPasswordError, MustBePositiveError, AlreadyExistsError
from security import security, get_hashed_password, is_correct_password


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
        :except MustBePositiveError
        """
        if limit <= 0 or page <= 0:
            raise MustBePositiveError('limit and page')
        return UserDAO.get_many(limit, page)

    @staticmethod
    def get_one_by_id_or_none(user_id: int) -> ReadUserS | None:
        return UserDAO.get_one_by_id_or_none(user_id)

    @staticmethod
    def login(data: LoginS) -> LoggedInS:
        """
        :except InvalidEmailOrPasswordError
        """
        user = security.datastore.find_user(email=data.email)

        if user is None or not is_correct_password(data.password, user.password):
            raise InvalidEmailOrPasswordError()

        access_token = create_access_token(identity=str(user.id))
        return LoggedInS(
            id=user.id,
            access_token=access_token,
            email=user.email,
            username=user.username,
            create_datetime=user.create_datetime,
            update_datetime=user.update_datetime,
        )


    @staticmethod
    def signup(user: CreateUserS) -> LoggedInS:
        """
        :except AlreadyExistsError
        """

        existed_user = security.datastore.find_user(email=user.email)
        if existed_user:
            raise AlreadyExistsError(f'User with email={user.email}')

        user_data = user.model_dump()
        user_data['password'] = get_hashed_password(user_data['password'])

        created_user = security.datastore.create_user(roles=['user'], **user_data)
        security.datastore.commit()

        access_token = create_access_token(identity=str(created_user.id))
        return LoggedInS(
            id=created_user.id,
            access_token=access_token,
            email=created_user.email,
            username=created_user.username,
            create_datetime=created_user.create_datetime,
            update_datetime=created_user.update_datetime,
        )

    @staticmethod
    def update_by_id(user_id: int, updated_user: BaseUserS) -> ReadUserS:
        """
        :except AlreadyExistsError
        :except WasNotFoundError
        """
        return UserDAO.update_by_id(user_id, updated_user)

    @staticmethod
    def delete_by_id(user_id: int) -> None:
        # user = security.datastore.find_user(id=user_id)
        # security.datastore.deactivate_user(user)
        # logout_user()
        # security.datastore.commit()
        return UserDAO.delete_by_id(user_id)
