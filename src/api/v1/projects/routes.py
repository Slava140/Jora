from typing import Union

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from api.v1.projects.schemas import CreateProjectS, ReadProjectS
from _types import Resp
from validation_decorator import validate
from api.v1.projects.services import ProjectService
from errors import WasNotFoundError
from global_schemas import HTTPError, PaginationQS, EmptyResponse

router = Blueprint(name='projects', import_name=__name__, url_prefix='/api/v1/projects')


@router.post('/')
@validate()
def add_project(body: CreateProjectS) -> Union[
    Resp[ReadProjectS, 201],
    Resp[HTTPError, 404],
]:
    try:
        created_project = ProjectService.add(body)
        return jsonify(created_project.model_dump()), 201

    except WasNotFoundError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 404


@router.get('/')
@jwt_required()
@validate()
def get_projects(query: PaginationQS) -> Union[
    Resp[ReadProjectS, 200],
    Resp[HTTPError, 400]
]:
    try:
        print(get_jwt())
        projects = ProjectService.get_many(query.limit, query.page)
        return jsonify([project.model_dump() for project in projects]), 200

    except ValueError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 400


@router.get('/<int:project_id>')
@validate()
def get_project_by_id(project_id: int) -> Union[
    Resp[ReadProjectS, 200],
    Resp[HTTPError, 404]
]:
    project = ProjectService.get_one_by_id_or_none(project_id)
    if project is None:
        return jsonify(HTTPError(message=f'Project with id {project_id} was not found.')), 404

    return jsonify(project.model_dump()), 200


@router.put('/<int:project_id>')
@validate()
def update_project_by_id(project_id: int, body: CreateProjectS) -> Union[
    Resp[ReadProjectS, 200],
    Resp[HTTPError, 404]
]:
    try:
        project = ProjectService.update_by_id(project_id, body)
        return jsonify(project.model_dump()), 200

    except WasNotFoundError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 404


@router.delete('/<int:project_id>')
@validate()
def delete_project_by_id(project_id: int) -> Resp[EmptyResponse, 202]:
    ProjectService.delete_by_id(project_id)
    return jsonify(), 204
