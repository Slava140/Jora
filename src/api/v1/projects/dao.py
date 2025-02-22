from datetime import datetime
from typing import Sequence

from sqlalchemy import insert, select, update, and_
from sqlalchemy.orm import SessionTransaction

from api.v1.projects.models import ProjectM, TaskM, CommentM
from api.v1.projects.schemas import (
    CreateProjectS, ReadProjectS, UpdateProjectS,
    CreateTaskS, ReadTaskS, UpdateTaskS,
    CreateCommentS, ReadCommentS, FilterTaskQS
)

from api.v1.users.dao import UserDAO
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
            if UserDAO.get_one_by_id_or_none(project.owner_id) is None:
                raise WasNotFoundError(f'Owner user with id {project.owner_id}')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadProjectS(**result)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadProjectS, ...]:
        query = select(
            ProjectM
        ).where(
            ProjectM.is_archived.is_(False)
        ).limit(limit).offset((page - 1) * limit)
        result = db.session.execute(query).scalars().fetchall()

        return tuple(ReadProjectS(**data.to_dict()) for data in result)

    @staticmethod
    def get_one_by_id_or_none(project_id: int) -> ReadProjectS | None:
        query = select(
            ProjectM
        ).where(
            ProjectM.id == project_id,
            ProjectM.is_archived.is_(False)
        )

        result = db.session.execute(query).scalar_one_or_none()

        return ReadProjectS(**result.to_dict()) if result is not None else None

    @staticmethod
    def update_by_id(project_id: int, updated_project: UpdateProjectS) -> ReadProjectS:
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

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadProjectS(**result)

    @staticmethod
    def delete_all_projects_with_user_id(
            user_id: int,
            transaction: SessionTransaction | None = None
    ) -> None:

        stmt = update(
            ProjectM
        ).where(
            ProjectM.owner_id == user_id
        ).values(
            is_archived=True
        ).returning(ProjectM.id)

        if transaction is None:
            transaction = db.session.begin()

        project_ids = transaction.session.execute(stmt).scalars().fetchall()
        TaskDAO.delete_all_tasks_with_project_ids(project_ids, transaction)

    @staticmethod
    def delete_by_id(project_id: int) -> None:
        stmt = update(
            ProjectM
        ).where(
            ProjectM.id == project_id
        ).values(
            is_archived=True
        ).returning(ProjectM.id)

        transaction = db.session.begin()
        project_ids = transaction.session.execute(stmt).scalars().fetchall()
        TaskDAO.delete_all_tasks_with_project_ids(project_ids, transaction)


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
            if UserDAO.get_one_by_id_or_none(task.author_id) is None:
                raise WasNotFoundError(f'Author user with id {task.author_id}')

            if ProjectDAO.get_one_by_id_or_none(task.project_id) is None:
                raise WasNotFoundError(f'Project with id {task.project_id}')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadTaskS(**result)

    @staticmethod
    def get_many(filter_schema: FilterTaskQS) -> tuple[ReadTaskS, ...]:
        where_conditions = []
        if filter_schema.project_id is not None: where_conditions.append(TaskM.project_id == filter_schema.project_id)
        if filter_schema.status is not None: where_conditions.append(TaskM.status == filter_schema.status)
        if filter_schema.author_id is not None: where_conditions.append(TaskM.author_id == filter_schema.author_id)
        if filter_schema.assignee_id is not None: where_conditions.append(TaskM.assignee_id == filter_schema.assignee_id)
        if filter_schema.title is not None: where_conditions.append(TaskM.title.ilike(filter_schema.title))
        if filter_schema.from_ is not None and filter_schema.to is not None:
            datetime_from = datetime.combine(filter_schema.from_, datetime.min.time())
            datetime_to = datetime.combine(filter_schema.to, datetime.max.time())
            where_conditions.append(TaskM.created_at.between(datetime_from, datetime_to))

        query = select(
            TaskM
        ).where(
            TaskM.is_archived.is_(False),
            *where_conditions
        ).limit(filter_schema.limit).offset((filter_schema.page - 1) * filter_schema.limit)
        result = db.session.execute(query).scalars().fetchall()

        return tuple(ReadTaskS(**data.to_dict()) for data in result)

    @staticmethod
    def get_one_by_id_or_none(task_id: int) -> ReadTaskS | None:
        query = select(
            TaskM
        ).where(
            TaskM.id == task_id,
            TaskM.is_archived.is_(False)
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

            assignee = UserDAO.get_one_by_id_or_none(updated_task.assignee_id)
            if assignee is None:
                raise WasNotFoundError(f'Assignee user with id {updated_task.assignee_id}')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadTaskS(**result)

    @staticmethod
    def delete_all_tasks_with_project_ids(
            project_ids: Sequence,
            transaction: SessionTransaction | None = None
    ) -> None:

        if len(project_ids) == 0:
            transaction.commit()
            return None

        stmt = update(
            TaskM
        ).where(
            TaskM.project_id.in_(project_ids)
        ).values(
            is_archived=True
        ).returning(TaskM.id)

        if transaction is None:
            transaction = db.session.begin()

        task_ids = transaction.session.execute(stmt).scalars().fetchall()
        CommentDAO.delete_all_comments_with_task_ids(task_ids, transaction)

    @staticmethod
    def delete_by_id(task_id: int) -> None:
        stmt = update(
            TaskM
        ).where(
            TaskM.id == task_id
        ).values(
            is_archived=True
        ).returning(TaskM.id)

        transaction = db.session.begin()
        task_ids = transaction.session.execute(stmt).scalars().fetchall()
        CommentDAO.delete_all_comments_with_task_ids(task_ids, transaction)


class CommentDAO:
    @staticmethod
    def add(comment: CreateCommentS) -> ReadCommentS:
        """
        :except WasNotFoundError
        """
        stmt = insert(
            CommentM
        ).values(
            **comment.model_dump()
        ).returning('*')

        with db.session.begin() as transaction:
            if UserDAO.get_one_by_id_or_none(comment.author_id) is None:
                raise WasNotFoundError(f"Author user with id {comment.author_id}")

            if TaskDAO.get_one_by_id_or_none(comment.task_id) is None:
                raise WasNotFoundError(f"Task with id {comment.task_id}")

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return ReadCommentS(**result)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadCommentS, ...]:
        query = select(
            CommentM
        ).where(
            CommentM.is_archived.is_(False)
        ).limit(limit).offset((page - 1) * limit)
        result = db.session.execute(query).scalars().fetchall()

        return tuple(ReadCommentS(**model.to_dict()) for model in result)

    @staticmethod
    def get_one_by_id_or_none(comment_id: int) -> ReadCommentS | None:
        query = select(
            CommentM
        ).where(
            CommentM.id == comment_id,
            CommentM.is_archived.is_(False)
        )

        result = db.session.execute(query).scalar_one_or_none()

        return ReadCommentS(**result.to_dict()) if result is not None else None

    @staticmethod
    def delete_all_comments_with_task_ids(
            task_ids: Sequence,
            transaction: SessionTransaction | None = None
    ) -> None:

        if len(task_ids) == 0:
            transaction.commit()
            return None

        stmt = update(
            CommentM
        ).where(
            CommentM.task_id.in_(task_ids)
        ).values(
            is_archived=True
        )

        if transaction is None:
            transaction = db.session.begin()

        transaction.session.execute(stmt)
        transaction.commit()
