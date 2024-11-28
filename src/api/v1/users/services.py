from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session

from api.v1.users.dao import UserDAO
from api.v1.users.schemas import CreateUserS


class UserService:
    dao = UserDAO()

    def add(self, user: CreateUserS):
        try:
            self.dao.insert(user)
        except ArgumentError as error:
            print(error.args)
