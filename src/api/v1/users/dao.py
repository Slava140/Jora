from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from api.v1.users.models import UserM
from api.v1.users.schemas import UserS


class UserDAO:
    model = UserM

    def insert(self, session: Session, user: UserS) -> None:
        stmt = insert(
            self.model
        ).values(
            **user
        )

        session.execute(stmt)
        session.commit()

    def get_one_by_id_or_none(self, session: Session, user_id: int) -> UserS | None:
        query = select(
            self.model
        ).where(
            self.model.id == user_id
        )

        result = session.execute(query).mappings().one_or_none()

        return UserS(**result) if result is not None else None


