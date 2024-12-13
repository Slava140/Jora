from typing import Union

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.v1.projects.services import ProjectService, TaskService
from api.v1.projects.schemas import (
    CreateProjectS, ReadProjectS,
    CreateTaskS, ReadTaskS, RequestBodyOfTaskS
)
from _types import Resp
from validation_decorator import validate
from errors import WasNotFoundError
from global_schemas import HTTPError, PaginationQS, EmptyResponse

projects_router = Blueprint(name='projects', import_name=__name__, url_prefix='/api/v1/projects')
tasks_router = Blueprint(name='tasks', import_name=__name__, url_prefix='/api/v1/tasks')


@projects_router.post('/')
@jwt_required()
@validate()
def add_project(body: CreateProjectS) -> Union[
    Resp[ReadProjectS, 201],
    Resp[HTTPError, 404],
]:
    created_project = ProjectService.add(body)
    return jsonify(created_project.model_dump()), 201


@projects_router.get('/')
@jwt_required()
@validate()
def get_projects(query: PaginationQS) -> Union[
    Resp[ReadProjectS, 200],
    Resp[HTTPError, 400]
]:
    projects = ProjectService.get_many(query.limit, query.page)
    return jsonify([project.model_dump() for project in projects]), 200


@projects_router.get('/<int:project_id>/')
@jwt_required()
@validate()
def get_project_by_id(project_id: int) -> Union[
    Resp[ReadProjectS, 200],
    Resp[HTTPError, 404]
]:
    project = ProjectService.get_one_by_id_or_none(project_id)
    if project is None:
        raise WasNotFoundError(f'Project with id {project_id}')

    return jsonify(project.model_dump()), 200


@projects_router.put('/<int:project_id>/')
@jwt_required()
@validate()
def update_project_by_id(project_id: int, body: CreateProjectS) -> Union[
    Resp[ReadProjectS, 200],
    Resp[HTTPError, 404]
]:
    project = ProjectService.update_by_id(project_id, body)
    return jsonify(project.model_dump()), 200


@projects_router.delete('/<int:project_id>/')
@jwt_required()
@validate()
def delete_project_by_id(project_id: int) -> Resp[EmptyResponse, 204]:
    ProjectService.delete_by_id(project_id)
    return jsonify(), 204


@tasks_router.post('/')
@jwt_required()
@validate()
def add_task(body: RequestBodyOfTaskS):
    author_id = get_jwt_identity()
    task_schema_with_author = CreateTaskS(author_id=author_id, **body.model_dump())
    created_task = TaskService.add(task_schema_with_author)
    return jsonify(**created_task.model_dump()), 201
