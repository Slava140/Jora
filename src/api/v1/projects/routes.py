from flask import jsonify
from flask_openapi3 import APIBlueprint
from flask_security import permissions_accepted, roles_accepted, current_user

from api.v1.projects.services import ProjectService, TaskService, CommentService
from api.v1.projects.schemas import (
    CreateProjectS, ReadProjectS, RequestBodyOfProjectS, UpdateProjectS, ProjectPath,
    CreateTaskS, ReadTaskS, RequestBodyOfTaskS, UpdateTaskS,
    CreateCommentS, ReadCommentS, RequestBodyOfCommentS, FilterTaskQS, TaskPath, CommentPath,
)
from errors import WasNotFoundError
from global_schemas import PaginationQS, security_schemas
from security import jwt_required

projects_router = APIBlueprint(
    name='projects', import_name=__name__, url_prefix='/api/v1/projects', abp_security=security_schemas
)

tasks_router = APIBlueprint(
    name='tasks', import_name=__name__, url_prefix='/api/v1/tasks', abp_security=security_schemas
)

comments_router = APIBlueprint(
    name='comments', import_name=__name__, url_prefix='/api/v1/comments', abp_security=security_schemas
)


@projects_router.post('/')
@jwt_required()
@permissions_accepted('project-write')
def add_project(body: RequestBodyOfProjectS):
    project_schema_with_owner = CreateProjectS(owner_id=current_user.id, **body.model_dump())
    created_project = ProjectService.add(project_schema_with_owner)
    return jsonify(created_project.model_dump()), 201


@projects_router.get('/')
@jwt_required()
@permissions_accepted('project-read')
def get_projects(query: PaginationQS):
    projects = ProjectService.get_many(query.limit, query.page)
    return jsonify([project.model_dump() for project in projects]), 200


@projects_router.get('/<int:project_id>/')
@jwt_required()
@permissions_accepted('project-read')
def get_project_by_id(path: ProjectPath):
    project = ProjectService.get_one_by_id_or_none(path.project_id)
    if project is None:
        raise WasNotFoundError(f'Project with id {path.project_id}')

    return jsonify(project.model_dump()), 200


@projects_router.put('/<int:project_id>/')
@jwt_required()
@permissions_accepted('project-write')
def update_project_by_id(path: ProjectPath, body: UpdateProjectS):
    project = ProjectService.update_by_id(path.project_id, body)
    return jsonify(project.model_dump()), 200


@projects_router.delete('/<int:project_id>/')
@jwt_required()
@permissions_accepted('project-write')
def delete_project_by_id(path: ProjectPath):
    ProjectService.delete_by_id(path.project_id)
    return jsonify(), 204


@tasks_router.post('/')
@jwt_required()
@permissions_accepted('task-write')
def add_task(body: RequestBodyOfTaskS):
    task_schema_with_author = CreateTaskS(author_id=current_user.id, **body.model_dump())
    created_task = TaskService.add(task_schema_with_author)
    return jsonify(**created_task.model_dump()), 201


@tasks_router.get('/')
@jwt_required()
@permissions_accepted('task-read')
def get_tasks(query: FilterTaskQS):
    tasks = TaskService.get_many(query)
    return jsonify([task.model_dump() for task in tasks]), 200


@tasks_router.get('/<int:task_id>/')
@jwt_required()
@permissions_accepted('task-read')
def get_task_by_id(path: TaskPath):
    task = TaskService.get_one_by_id_or_none(path.task_id)
    if task is None:
        raise WasNotFoundError(f'Task with id {path.task_id}')

    return jsonify(task.model_dump()), 200


@tasks_router.put('/<int:task_id>/')
@jwt_required()
@permissions_accepted('task-write')
def update_task_by_id(path: TaskPath, body: UpdateTaskS):
    task = TaskService.update_by_id(path.task_id, body)
    return jsonify(task.model_dump()), 200


@tasks_router.delete('/<int:task_id>/')
@jwt_required()
@permissions_accepted('task-write')
def delete_task_by_id(path: TaskPath):
    TaskService.delete_by_id(path.task_id)
    return jsonify(), 204


@comments_router.post('/')
@jwt_required()
@roles_accepted('admin', 'user')
def add_comment(body: RequestBodyOfCommentS):
    comment_schema_with_author = CreateCommentS(author_id=current_user.id, **body.model_dump())
    created_comment = CommentService.add(comment_schema_with_author)
    return jsonify(created_comment.model_dump()), 201


@comments_router.get('/')
@jwt_required()
@roles_accepted('admin', 'user')
def get_comments(query: PaginationQS):
    comments = CommentService.get_many(query.limit, query.page)
    return jsonify([comment.model_dump() for comment in comments]), 200


@comments_router.get('/<int:comment_id>/')
@jwt_required()
@roles_accepted('admin', 'user')
def get_comment_by_id(path: CommentPath):
    comment = CommentService.get_one_by_id_or_none(path.comment_id)
    if comment is None:
        raise WasNotFoundError(f'Comment with id {path.comment_id}')

    return jsonify(comment.model_dump()), 200
