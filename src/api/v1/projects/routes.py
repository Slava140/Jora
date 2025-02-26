from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_openapi3 import APIBlueprint

from api.v1.projects.services import ProjectService, TaskService, CommentService
from api.v1.projects.schemas import (
    CreateProjectS, ReadProjectS, RequestBodyOfProjectS, UpdateProjectS, ProjectPath,
    CreateTaskS, ReadTaskS, RequestBodyOfTaskS, UpdateTaskS,
    CreateCommentS, ReadCommentS, RequestBodyOfCommentS, FilterTaskQS,
)
from errors import WasNotFoundError
from global_schemas import PaginationQS
from security import security


projects_router = APIBlueprint(
    name='projects', import_name=__name__, url_prefix='/api/v1/projects', abp_security=security
)

tasks_router = APIBlueprint(
    name='tasks', import_name=__name__, url_prefix='/api/v1/tasks', abp_security=security
)

comments_router = APIBlueprint(
    name='comments', import_name=__name__, url_prefix='/api/v1/comments', abp_security=security
)


@projects_router.post('/')
@jwt_required()
def add_project(body: RequestBodyOfProjectS):
    owner_id = get_jwt_identity()
    project_schema_with_owner = CreateProjectS(owner_id=owner_id, **body.model_dump())
    created_project = ProjectService.add(project_schema_with_owner)
    return jsonify(created_project.model_dump()), 201


@projects_router.get('/')
@jwt_required()
def get_projects(query: PaginationQS):
    projects = ProjectService.get_many(query.limit, query.page)
    return jsonify([project.model_dump() for project in projects]), 200


@projects_router.get('/<int:project_id>/')
@jwt_required()
def get_project_by_id(path: ProjectPath):
    project = ProjectService.get_one_by_id_or_none(path.project_id)
    if project is None:
        raise WasNotFoundError(f'Project with id {path.project_id}')

    return jsonify(project.model_dump()), 200


@projects_router.put('/<int:project_id>/')
@jwt_required()
def update_project_by_id(path: ProjectPath, body: UpdateProjectS):
    project = ProjectService.update_by_id(path.project_id, body)
    return jsonify(project.model_dump()), 200


@projects_router.delete('/<int:project_id>/')
@jwt_required()
def delete_project_by_id(path: ProjectPath):
    # Может только владелец
    ProjectService.delete_by_id(path.project_id)
    return jsonify(), 204


@tasks_router.post('/')
@jwt_required()
def add_task(body: RequestBodyOfTaskS):
    # Может любой
    author_id = get_jwt_identity()
    task_schema_with_author = CreateTaskS(author_id=author_id, **body.model_dump())
    created_task = TaskService.add(task_schema_with_author)
    return jsonify(**created_task.model_dump()), 201


@tasks_router.get('/')
@jwt_required()
def get_tasks(query: FilterTaskQS):
    # Может любой
    tasks = TaskService.get_many(query)
    return jsonify([task.model_dump() for task in tasks]), 200


@tasks_router.get('/<int:task_id>/')
@jwt_required()
def get_task_by_id(task_id: int):
    # Может любой
    task = TaskService.get_one_by_id_or_none(task_id)
    if task is None:
        raise WasNotFoundError(f'Task with id {task_id}')

    return jsonify(task.model_dump()), 200


@tasks_router.put('/<int:task_id>/')
@jwt_required()
def update_task_by_id(task_id: int, body: UpdateTaskS):
    # Владелец задачи
    task = TaskService.update_by_id(task_id, body)
    return jsonify(task.model_dump()), 200


@tasks_router.delete('/<int:task_id>/')
@jwt_required()
def delete_task_by_id(task_id: int):
    # Владелец задачи
    TaskService.delete_by_id(task_id)
    return jsonify(), 204


@comments_router.post('/')
@jwt_required()
def add_comment(body: RequestBodyOfCommentS):
    # Любой пользователь
    author_id = get_jwt_identity()
    comment_schema_with_author = CreateCommentS(author_id=author_id, **body.model_dump())
    created_comment = CommentService.add(comment_schema_with_author)
    return jsonify(created_comment.model_dump()), 201


@comments_router.get('/')
@jwt_required()
def get_comments(query: PaginationQS):
    comments = CommentService.get_many(query.limit, query.page)
    return jsonify([comment.model_dump() for comment in comments]), 200


@comments_router.get('/<int:comment_id>/')
@jwt_required()
def get_comment_by_id(comment_id: int):
    comment = CommentService.get_one_by_id_or_none(comment_id)
    if comment is None:
        raise WasNotFoundError(f'Comment with id {comment_id}')

    return jsonify(comment.model_dump()), 200
