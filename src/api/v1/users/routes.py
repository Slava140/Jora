from typing import Union

from flask import Blueprint, jsonify, request

from api.v1.users.services import UserService
from api.v1.users.schemas import CreateUserS, BaseUserS, ReadUserS, LoginS, LoggedInS
from _types import Resp
from validation_decorator import validate
from errors import AlreadyExistsError, WasNotFoundError, InvalidEmailOrPasswordError
from global_schemas import HTTPError, EmptyResponse, PaginationQS


router = Blueprint(name='users', import_name=__name__, url_prefix='/api/v1/users')
auth_router = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@router.post('/')
@validate()
def add_user(body: CreateUserS) -> Union[
    Resp[ReadUserS, 201],
    Resp[HTTPError, 409]
]:
    try:
        created_user = UserService.add(body)
        return jsonify(created_user.model_dump()), 201

    except AlreadyExistsError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 409


@router.get('/')
@validate()
def get_users(query: PaginationQS) -> Union[
    Resp[ReadUserS, 200],
    Resp[HTTPError, 400]
]:
    try:
        users = UserService.get_many(query.limit, query.page)
        return jsonify([user.model_dump() for user in users]), 200

    except ValueError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 400


@router.get('/<int:user_id>')
@validate()
def get_user_by_id(user_id: int) -> Union[
    Resp[ReadUserS, 200],
    Resp[HTTPError, 404]
]:
    user = UserService.get_one_by_id_or_none(user_id)
    if user is None:
        return jsonify(HTTPError(message='User was not found.').model_dump()), 404

    return jsonify(user.model_dump()), 200


@router.put('/<int:user_id>')
@validate()
def update_user_by_id(user_id: int, body: BaseUserS) -> Union[
    Resp[ReadUserS, 200],
    Resp[HTTPError, 404],
    Resp[HTTPError, 409]
]:
    try:
        user = UserService.update_by_id(int(user_id), body)
        return jsonify(user.model_dump()), 200

    except AlreadyExistsError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 409

    except WasNotFoundError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 404


@router.delete('/<int:user_id>')
@validate()
def delete_user_by_id(user_id: int) -> Resp[EmptyResponse, 202]:
    UserService.delete_by_id(user_id)
    return jsonify({}), 202


@auth_router.post('/login')
@validate()
def login(body: LoginS) -> Union[
    Resp[LoggedInS, 200],
    Resp[HTTPError, 401]
]:
    try:
        logged_in_user = UserService.login(body)
        return jsonify(logged_in_user.model_dump()), 200
    except InvalidEmailOrPasswordError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 401
