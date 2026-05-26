import json
import os
import tempfile
from pathlib import Path

from flask import url_for
from flask_openapi3 import FileStorage
from werkzeug.utils import secure_filename

from api.v1.projects.dao import ProjectDAO, TaskDAO, CommentDAO
from api.v1.projects.models import Status
from api.v1.projects.schemas import (
    CreateProjectS, ReadProjectS, UpdateProjectS,
    CreateTaskS, ReadTaskS, UpdateTaskS,
    CreateCommentS, ReadCommentS, FilterTaskQS, ReadTaskWithMedia, ExportProjectS, FilterCommentQS, ExportTaskS,
    ExportCommentS,
)
from flask_security import current_user

from api.v1.users.schemas import ReadUserS
from errors import MustBePositiveError, IncorrectRequestError, ForbiddenError, WasNotFoundError, \
    ExtensionsNotAllowedError


class ProjectService:
    @staticmethod
    def add(project: CreateProjectS) -> ReadProjectS:
        """
        :except WasNotFoundError
        """
        return ProjectDAO.add(project)

    @staticmethod
    def get_many(user_id: int, limit: int, page: int) -> tuple[ReadProjectS, ...]:
        """
        :except MustBePositiveError
        """
        if limit <= 0 or page <= 0:
            raise MustBePositiveError('limit and page')

        return ProjectDAO.get_many(user_id, limit, page)

    @staticmethod
    def get_one_by_id_or_none(user_id: int, project_id: int) -> ReadProjectS | None:
        project = ProjectDAO.get_one_by_id_or_none(project_id=project_id)
        if not project:
            return None

        project_users = ProjectDAO.get_users(project_id=project_id)
        if user_id not in [u.id for u in project_users]:
            return None

        return project

    @staticmethod
    def get_users(user_id: int, project_id: int) -> list[ReadUserS]:
        project_users = ProjectDAO.get_users(project_id=project_id)
        if user_id in project_users:
            return project_users

        else:
            raise ForbiddenError()


    @staticmethod
    def update_by_id(user_id: int, project_id: int, updated_project: UpdateProjectS) -> ReadProjectS | None:
        return ProjectDAO.update_by_id(
            user_id=user_id,
            project_id=project_id,
            updated_project=updated_project,
        )

    @staticmethod
    def delete_by_id(user_id: int, project_id: int) -> None:
        ProjectDAO.delete_by_id(user_id, project_id)

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

    @staticmethod
    def import_(file: FileStorage):
        tmp_path = Path(tempfile.gettempdir())
        destination_path = tmp_path / secure_filename(file.filename)

        if destination_path.suffix != '.json':
            raise ExtensionsNotAllowedError

        file.save(destination_path)
        with open(destination_path, 'r', encoding='utf-8') as imported_json:
            json_str = json.load(imported_json)
            imported_project = ExportProjectS.model_validate(json_str)
            os.remove(destination_path)

        ProjectDAO.import_(owner_id=current_user.id, schema=imported_project)

class TaskService:
    @staticmethod
    def add(user_id: int, task: CreateTaskS) -> ReadTaskS:
        """
        :except WasNotFoundError
        """
        project_users = ProjectDAO.get_users(project_id=task.project_id)
        if user_id not in [u.id for u in project_users]:
            raise ForbiddenError()
        return TaskDAO.add(task=task)

    @staticmethod
    def get_many(user_id: int, filter_schema: FilterTaskQS) -> list[ReadTaskWithMedia]:
        """
        :except MustBePositiveError
        :except IncorrectRequestError
        """
        if filter_schema.limit <= 0 or filter_schema.page <= 0:
            raise MustBePositiveError('limit and page')

        if (filter_schema.from_ is None and filter_schema.to is not None or
            filter_schema.from_ is not None and filter_schema.to is None):
            raise IncorrectRequestError('from and to parameters must be filled or empty')

        return TaskDAO.get_many(user_id=user_id, filter_schema=filter_schema)

    @staticmethod
    def get_one_by_id_or_none(user_id: int, task_id: int) -> ReadTaskWithMedia | None:
        task = TaskDAO.get_one_by_id_or_none(task_id)
        if not task:
            return None

        if user_id in (task.author_id, task.assignee_id):
            return task
        else:
            return None

    @staticmethod
    def update_by_id(user_id: int, task_id: int, body: UpdateTaskS) -> ReadTaskS:
        task = TaskDAO.get_one_by_id_or_none(task_id)
        if not task:
            raise WasNotFoundError(f'Task with id {task_id}')

        project = ProjectDAO.get_one_by_id_or_none(task.project_id)
        if not project:
            raise WasNotFoundError(f'Project with id {task_id}')

        if user_id not in (task.author_id, task.assignee_id, project.owner_id):
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
    def delete_by_id(user_id: int, task_id: int) -> None:
        TaskDAO.delete_by_id(user_id=user_id, task_id=task_id)


class CommentService:
    @staticmethod
    def add(user_id: int, comment: CreateCommentS) -> ReadCommentS:
        """
        :except WasNotFoundError
        """
        task = TaskDAO.get_one_by_id_or_none(task_id=comment.task_id)
        if not task:
            raise WasNotFoundError(f'Task with id {comment.task_id}')

        project_users = ProjectDAO.get_users(project_id=task.project_id)

        if user_id not in [u.id for u in project_users]:
            raise ForbiddenError()
        return CommentDAO.add(comment)

    @staticmethod
    def get_many(user_id: int, filter_schema: FilterCommentQS) -> tuple[ReadCommentS, ...]:
        """
        :except MustBePositiveError
        """
        if filter_schema.limit <= 0 or filter_schema.page <= 0:
            raise MustBePositiveError('limit and page')
        return CommentDAO.get_many(
            user_id=user_id,
            filter_schema=filter_schema,
        )

    @staticmethod
    def get_one_by_id_or_none(user_id: int, comment_id: int) -> ReadCommentS | None:
        comment = CommentDAO.get_one_by_id_or_none(comment_id=comment_id)
        if not comment:
            return None

        task = TaskService.get_one_by_id_or_none(user_id=user_id, task_id=comment.task_id)
        if not task:
            raise WasNotFoundError(f'Task with id {comment.task_id}')

        project_users = ProjectService.get_users(
            user_id=user_id,
            project_id=task.project_id
        )

        if user_id not in [u.id for u in project_users]:
            raise ForbiddenError()

        return comment


if __name__ == '__main__':
    from app import app

    with app.app_context():
        print(ProjectService().get_one_by_id_or_none(2, 1))