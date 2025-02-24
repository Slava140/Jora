from api.v1.projects.dao import ProjectDAO, TaskDAO, CommentDAO
from api.v1.projects.schemas import (
    CreateProjectS, ReadProjectS, UpdateProjectS,
    CreateTaskS, ReadTaskS, UpdateTaskS,
    CreateCommentS, ReadCommentS, FilterTaskQS,
)
from errors import MustBePositiveError, IncorrectRequestError


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


class TaskService:
    @staticmethod
    def add(task: CreateTaskS) -> ReadTaskS:
        """
        :except WasNotFoundError
        """
        return TaskDAO.add(task)

    @staticmethod
    def get_many(filter_schema: FilterTaskQS) -> tuple[ReadTaskS, ...]:
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
