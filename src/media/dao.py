from sqlalchemy import insert, select

from media.models import MediaM
from media.schemas import ReadMediaS, CreateMediaS

from api.v1.users.services import UserService
from api.v1.projects.services import TaskService

from database import db
from errors import WasNotFoundError


class MediaDAO:
    @staticmethod
    def add(media_metadata: CreateMediaS) -> ReadMediaS:
        """
        Для завершения транзакции ОБЯЗАТЕЛЬНО нужно выполнить commit или rollback.
        Транзакцию нельзя завершить внутри этого метода, потому что возможен сценарий при котором
        запись добавлена в БД, а файл из-за ошибки не был сохранен в файловой системе.

        :except WasNotFoundError
        """
        stmt = insert(
            MediaM
        ).values(
            **media_metadata.model_dump()
        ).returning('*')

        with db.session.begin(nested=True):
            if not UserService.get_one_by_id_or_none(media_metadata.author_id):
                raise WasNotFoundError(f'Author user with id {media_metadata.author_id}')

            if not TaskService.get_one_by_id_or_none(
                    user_id=media_metadata.author_id,
                    task_id=media_metadata.task_id
            ):
                raise WasNotFoundError(f'Task with id {media_metadata.task_id}')

            result = db.session.execute(stmt).mappings().one()

        return ReadMediaS(**result)

    @staticmethod
    def get_one_by_id_or_none(media_id: int) -> ReadMediaS | None:
        query = select(
            MediaM
        ).where(
            MediaM.id == media_id
        )

        result = db.session.execute(query).scalar_one_or_none()

        return ReadMediaS(**result.to_dict()) if result is not None else None
