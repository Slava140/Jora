from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from api.v1.users.models import UserM
from api.v1.users.schemas import CreateUserS, ReadUserS
from api.v1.auth.utils import get_hashed_password


class UserDAO:
    model = UserM

    def insert(self, session: Session, user: CreateUserS) -> None:
        stmt = insert(
            self.model
        ).values(
            email=user.email,
            username=user.username,
            hashed_password=get_hashed_password(user.password)
        )

        session.execute(stmt)
        session.commit()

    def get_one_by_id_or_none(self, session: Session, user_id: int) -> ReadUserS | None:
        query = select(
            self.model
        ).where(
            self.model.id == user_id
        )

        result = session.execute(query).mappings().one_or_none()

        return ReadUserS(**result) if result is not None else None


