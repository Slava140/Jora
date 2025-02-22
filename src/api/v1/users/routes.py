from typing import Union

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt, set_access_cookies

from api.v1.users.services import UserService
from api.v1.users.schemas import CreateUserS, BaseUserS, ReadUserS, LoginS, LoggedInS
from _types import Resp
from validation_decorator import validate
from errors import WasNotFoundError
from global_schemas import HTTPError, EmptyResponse, PaginationQS


router = Blueprint(name='users', import_name=__name__, url_prefix='/api/v1/users')
auth_router = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@router.post('/')
@jwt_required()
@validate()
def add_user(body: CreateUserS) -> Union[
    Resp[ReadUserS, 201],
    Resp[HTTPError, 409]
]:
    created_user = UserService.add(body)
    return jsonify(created_user.model_dump()), 201


@router.get('/')
@jwt_required()
@validate()
def get_users(query: PaginationQS) -> Union[
    Resp[ReadUserS, 200],
    Resp[HTTPError, 400]
]:
    users = UserService.get_many(query.limit, query.page)
    return jsonify([user.model_dump() for user in users]), 200


@router.get('/<int:user_id>/')
@jwt_required()
@validate()
def get_user_by_id(user_id: int) -> Union[
    Resp[ReadUserS, 200],
    Resp[HTTPError, 404]
]:
    user = UserService.get_one_by_id_or_none(user_id)
    if user is None:
        raise WasNotFoundError(f'User with id {user_id}')

    return jsonify(user.model_dump()), 200


@router.put('/<int:user_id>/')
@jwt_required()
@validate()
def update_user_by_id(user_id: int, body: BaseUserS) -> Union[
    Resp[ReadUserS, 200],
    Resp[HTTPError, 404],
    Resp[HTTPError, 409]
]:
    user = UserService.update_by_id(user_id, body)
    return jsonify(user.model_dump()), 200


@router.delete('/<int:user_id>/')
@jwt_required()
@validate()
def delete_user_by_id(user_id: int) -> Resp[EmptyResponse, 204]:
    UserService.delete_by_id(user_id)
    return jsonify(), 204


@auth_router.post('/login/')
@validate()
def login(body: LoginS) -> Union[
    Resp[LoggedInS, 200],
    Resp[HTTPError, 401]
]:
    logged_in_user = UserService.login(body)
    response = jsonify(logged_in_user.model_dump())
    set_access_cookies(response, logged_in_user.access_token)
    return response, 200


@auth_router.post('/signup/')
@validate()
def signup(body: CreateUserS) -> Union[
    Resp[LoggedInS, 201],
    Resp[HTTPError, 409]
]:
    logged_in_user = UserService.signup(body)
    response = jsonify(logged_in_user.model_dump())
    set_access_cookies(response, logged_in_user.access_token)
    return response, 201
