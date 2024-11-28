from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session

from api.v1.users.dao import UserDAO
from api.v1.users.schemas import CreateUserS


class UserService:
    dao = UserDAO()

    def add(self, session: Session, user: CreateUserS):

        try:
            self.dao.insert(session, user)
        except ArgumentError as error:
            print(error.args)
