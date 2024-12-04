from typing import Any

from sqlalchemy import insert, select, and_, update, delete
from sqlalchemy.orm import InstrumentedAttribute, Session

from api.v1.projects.models import ProjectM
from api.v1.projects.schemas import CreateProjectS, ReadProjectS
from api.v1.users.services import UserService
from database import get_db
from errors import WasNotFoundError


class ProjectDAO:
    @staticmethod
    def get_one(
            where: tuple[InstrumentedAttribute, Any],
            exclude_where: tuple[InstrumentedAttribute, Any] | None = None,
            session: Session | None = None) -> ProjectM | None:

        session = next(get_db()) if session is None else session
        if exclude_where is None:
            query = select(ProjectM).where(where[0] == where[1]).limit(1)
        else:
            query = select(
                ProjectM
            ).where(
                and_(
                    where[0] == where[1],
                    exclude_where[0].not_in([exclude_where[1]])
                )
            ).limit(1)
        return session.execute(query).scalar_one_or_none()

    @staticmethod
    def add(project: CreateProjectS) -> ReadProjectS:
        """
        :except WasNotFoundError
        """
        stmt = insert(
            ProjectM
        ).values(
            **project.model_dump()
        ).returning('*')

        with next(get_db()) as session:
            if UserService.get_one_by_id_or_none(project.owner_id) is None:
                raise WasNotFoundError(f'Owner user with id {project.owner_id}')

            result = session.execute(stmt).mappings().one()
            session.commit()

        return ReadProjectS(**result)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadProjectS, ...]:
        query = select(ProjectM).limit(limit).offset((page - 1) * limit)
        with next(get_db()) as session:
            result = session.execute(query).scalars().fetchall()
        return tuple(ReadProjectS(**data.to_dict()) for data in result)

    @staticmethod
    def get_one_by_id_or_none(project_id: int) -> ReadProjectS | None:
        query = select(
            ProjectM
        ).where(
            ProjectM.id == project_id
        )

        with next(get_db()) as session:
            result = session.execute(query).scalar_one_or_none()

        return ReadProjectS(**result.to_dict()) if result is not None else None

    @staticmethod
    def update_by_id(project_id: int, updated_project: CreateProjectS) -> ReadProjectS:
        """
        :except WasNotFoundError
        """
        stmt = update(
            ProjectM
        ).where(
            ProjectM.id == project_id
        ).values(
            **updated_project.model_dump()
        ).returning('*')

        with next(get_db()) as session:
            project = ProjectDAO.get_one(where=(ProjectM.id, project_id), session=session)

            if project is None:
                raise WasNotFoundError(f'Project with id={project_id}')

            owner_user = UserService.get_one_by_id_or_none(updated_project.owner_id)

            if owner_user is None:
                raise WasNotFoundError(f'Owner user with id {updated_project.owner_id}')

            result = session.execute(stmt).mappings().one()
            session.commit()

        return ReadProjectS(**result)

    @staticmethod
    def delete_by_id(project_id: int) -> None:
        stmt = delete(ProjectM).where(ProjectM.id == project_id)

        with next(get_db()) as session:
            session.execute(stmt)
            session.commit()

        return None
