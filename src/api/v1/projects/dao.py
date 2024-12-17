from sqlalchemy import insert, select, update, delete

from api.v1.projects.models import ProjectM, TaskM
from api.v1.projects.schemas import (
    CreateProjectS, ReadProjectS,
    CreateTaskS, ReadTaskS, UpdateTaskS,
)

from api.v1.users.services import UserService
from errors import WasNotFoundError
from database import db


class ProjectDAO:
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

        with db.session.begin() as transaction:
            if UserService.get_one_by_id_or_none(project.owner_id) is None:
                raise WasNotFoundError(f'Owner user with id {project.owner_id}')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadProjectS(**result)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadProjectS, ...]:
        query = select(ProjectM).limit(limit).offset((page - 1) * limit)
        result = db.session.execute(query).scalars().fetchall()

        return tuple(ReadProjectS(**data.to_dict()) for data in result)

    @staticmethod
    def get_one_by_id_or_none(project_id: int) -> ReadProjectS | None:
        query = select(
            ProjectM
        ).where(
            ProjectM.id == project_id
        )

        result = db.session.execute(query).scalar_one_or_none()

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

        with db.session.begin() as transaction:
            project = ProjectDAO.get_one_by_id_or_none(project_id)

            if project is None:
                raise WasNotFoundError(f'Project with id {project_id}')

            owner_user = UserService.get_one_by_id_or_none(updated_project.owner_id)

            if owner_user is None:
                raise WasNotFoundError(f'Owner user with id {updated_project.owner_id}')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadProjectS(**result)

    @staticmethod
    def delete_by_id(project_id: int) -> None:
        stmt = delete(ProjectM).where(ProjectM.id == project_id)

        db.session.execute(stmt)
        db.session.commit()

        return None


class TaskDAO:
    @staticmethod
    def add(task: CreateTaskS) -> ReadTaskS:
        """
        :except WasNotFoundError
        """
        stmt = insert(
            TaskM
        ).values(
            **task.model_dump()
        ).returning('*')

        with db.session.begin() as transaction:
            if UserService.get_one_by_id_or_none(task.author_id) is None:
                raise WasNotFoundError(f'Author with id {task.author_id}')
            if ProjectDAO.get_one_by_id_or_none(task.project_id) is None:
                raise WasNotFoundError(f'Project with id {task.project_id}')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadTaskS(**result)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadTaskS, ...]:
        query = select(TaskM).limit(limit).offset((page - 1) * limit)
        result = db.session.execute(query).scalars().fetchall()

        return tuple(ReadTaskS(**data.to_dict()) for data in result)

    @staticmethod
    def get_one_by_id_or_none(task_id: int) -> ReadTaskS | None:
        query = select(
            TaskM
        ).where(
            TaskM.id == task_id
        )

        result = db.session.execute(query).scalar_one_or_none()

        return ReadTaskS(**result.to_dict()) if result is not None else None

    @staticmethod
    def update_by_id(task_id: int, updated_task: UpdateTaskS) -> ReadTaskS:
        """
        :except WasNotFoundError
        """
        stmt = update(
            TaskM
        ).where(
            TaskM.id == task_id
        ).values(
            **updated_task.model_dump()
        ).returning('*')

        with db.session.begin() as transaction:
            task = TaskDAO.get_one_by_id_or_none(task_id)
            if task is None:
                raise WasNotFoundError(f'Task with id {task_id}')

            assignee = UserService.get_one_by_id_or_none(updated_task.assignee_id)
            if assignee is None:
                raise WasNotFoundError(f'Assignee user with id {updated_task.assignee_id}')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadTaskS(**result)
