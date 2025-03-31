from flask import url_for

from api.v1.projects.dao import ProjectDAO, TaskDAO, CommentDAO
from api.v1.projects.models import Status
from api.v1.projects.schemas import (
    CreateProjectS, ReadProjectS, UpdateProjectS,
    CreateTaskS, ReadTaskS, UpdateTaskS,
    CreateCommentS, ReadCommentS, FilterTaskQS, ReadTaskWithMedia, ExportProjectS, FilterCommentQS, ExportTaskS,
    ExportCommentS,
)
from flask_security import current_user
from errors import MustBePositiveError, IncorrectRequestError, ForbiddenError, WasNotFoundError


class ProjectService:
    @staticmethod
    def add(project: CreateProjectS) -> ReadProjectS:
        """
        :except WasNotFoundError
        """
        return ProjectDAO.add(project)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadProjectS, ...]:
        """
        :except MustBePositiveError
        """
        if limit <= 0 or page <= 0:
            raise MustBePositiveError('limit and page')
        return ProjectDAO.get_many(limit, page)

    @staticmethod
    def get_one_by_id_or_none(project_id: int) -> ReadProjectS | None:
        return ProjectDAO.get_one_by_id_or_none(project_id)

    @staticmethod
    def update_by_id(project_id: int, updated_project: UpdateProjectS) -> ReadProjectS:
        """
        :except WasNotFoundError
        """
        return ProjectDAO.update_by_id(project_id, updated_project)

    @staticmethod
    def delete_by_id(project_id: int) -> None:
        return ProjectDAO.delete_by_id(project_id)

    @staticmethod
    def export(project_id: int) -> ExportProjectS:
        project = ProjectDAO.get_one_by_id_or_none(project_id)
        tasks = TaskService.get_many(filter_schema=FilterTaskQS(project_id=project_id))
        exported_tasks = []
        for task in tasks:
            comments = CommentService.get_many(filter_schema=FilterCommentQS(task_id=task.id))
            exported_task = ExportTaskS(
                **task.model_dump(),
                comments=[ExportCommentS(**comment.model_dump()) for comment in comments]
            )
            exported_tasks.append(exported_task)

        return ExportProjectS(**project.model_dump(), tasks=exported_tasks)


class TaskService:
    @staticmethod
    def add(task: CreateTaskS) -> ReadTaskS:
        """
        :except WasNotFoundError
        """
        return TaskDAO.add(task)

    @staticmethod
    def get_many(filter_schema: FilterTaskQS) -> list[ReadTaskWithMedia]:
        """
        :except MustBePositiveError
        :except IncorrectRequestError
        """
        if filter_schema.limit <= 0 or filter_schema.page <= 0:
            raise MustBePositiveError('limit and page')

        if (filter_schema.from_ is None and filter_schema.to is not None or
            filter_schema.from_ is not None and filter_schema.to is None):
            raise IncorrectRequestError('from and to parameters must be filled or empty')

        return TaskDAO.get_many(filter_schema)

    @staticmethod
    def get_one_by_id_or_none(task_id: int) -> ReadTaskWithMedia | None:
        return TaskDAO.get_one_by_id_or_none(task_id)

    @staticmethod
    def update_by_id(task_id: int, body: UpdateTaskS) -> ReadTaskS:
        task = TaskDAO.get_one_by_id_or_none(task_id)

        if task is None:
            raise WasNotFoundError('Task')

        is_current_user_author_or_admin = current_user.id == task.author_id or 'admin' in current_user.roles
        is_current_user_assignee = current_user.id == task.assignee_id
        if not is_current_user_author_or_admin and not is_current_user_assignee:
            raise ForbiddenError()

        updated_task = TaskDAO.update_by_id(task_id, body)

        is_assignee_changed = updated_task.assignee_id != task.assignee_id
        if updated_task.assignee_id is not None and is_assignee_changed:
            from actors import send_notification_actor
            send_notification_actor.send(
                recipient_user_id=updated_task.assignee_id,
                subject='Вы были назначены исполнителем.',
                task_id=updated_task.id,
                task_url=url_for('tasks.get_task_by_id', task_id=task_id, _external=True)
            )

        if Status(task.status) > Status(updated_task.status):
            from actors import send_notification_actor
            send_notification_actor.send(
                recipient_user_id=updated_task.author_id,
                subject='Изменен статус задачи.',
                task_id=updated_task.id,
                task_url=url_for('tasks.get_task_by_id', task_id=task_id, _external=True)
            )

        return updated_task

    @staticmethod
    def delete_by_id(task_id: int) -> None:
        task = TaskDAO.get_one_by_id_or_none(task_id)
        if task is None:
            return None
        if task.author_id != current_user.id and 'admin' not in current_user.roles:
            raise ForbiddenError()
        return TaskDAO.delete_by_id(task_id)


class CommentService:
    @staticmethod
    def add(comment: CreateCommentS) -> ReadCommentS:
        """
        :except WasNotFoundError
        """
        return CommentDAO.add(comment)

    @staticmethod
    def get_many(filter_schema: FilterCommentQS) -> tuple[ReadCommentS, ...]:
        """
        :except MustBePositiveError
        """
        if filter_schema.limit <= 0 or filter_schema.page <= 0:
            raise MustBePositiveError('limit and page')
        return CommentDAO.get_many(filter_schema)

    @staticmethod
    def get_one_by_id_or_none(comment_id: int) -> ReadCommentS | None:
        return CommentDAO.get_one_by_id_or_none(comment_id)
