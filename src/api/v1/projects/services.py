from api.v1.projects.dao import ProjectDAO, TaskDAO, CommentDAO
from api.v1.projects.schemas import (
    CreateProjectS, ReadProjectS,
    CreateTaskS, ReadTaskS, UpdateTaskS,
    CreateCommentS, ReadCommentS,
)
from errors import MustBePositiveError


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
    def update_by_id(project_id: int, updated_project: CreateProjectS) -> ReadProjectS:
        """
        :except WasNotFoundError
        """
        return ProjectDAO.update_by_id(project_id, updated_project)

    @staticmethod
    def delete_by_id(project_id: int) -> None:
        return ProjectDAO.delete_by_id(project_id)


class TaskService:
    @staticmethod
    def add(task: CreateTaskS) -> ReadTaskS:
        """
        :except WasNotFoundError
        """
        return TaskDAO.add(task)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadTaskS, ...]:
        """
        :except MustBePositiveError
        """
        if limit <= 0 or page <= 0:
            raise MustBePositiveError('limit and page')
        return TaskDAO.get_many(limit, page)

    @staticmethod
    def get_one_by_id_or_none(task_id: int) -> ReadTaskS | None:
        return TaskDAO.get_one_by_id_or_none(task_id)

    @staticmethod
    def update_by_id(task_id: int, updated_task: UpdateTaskS) -> ReadTaskS:
        """
        :except WasNotFoundError
        """
        return TaskDAO.update_by_id(task_id, updated_task)

    @staticmethod
    def delete_by_id(project_id: int) -> None:
        return TaskDAO.delete_by_id(project_id)


class CommentService:
    @staticmethod
    def add(comment: CreateCommentS) -> ReadCommentS:
        """
        :except WasNotFoundError
        """
        return CommentDAO.add(comment)

    @staticmethod
    def get_many(limit: int, page: int) -> tuple[ReadCommentS, ...]:
        """
        :except MustBePositiveError
        """
        if limit <= 0 or page <= 0:
            raise MustBePositiveError('limit and page')
        return CommentDAO.get_many(limit, page)

    @staticmethod
    def get_one_by_id_or_none(comment_id: int) -> ReadCommentS | None:
        return CommentDAO.get_one_by_id_or_none(comment_id)
