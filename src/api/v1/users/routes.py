import pydantic
from flask import Blueprint, request, jsonify

from api.v1.users.services import UserService
from api.v1.users.schemas import CreateUserS, BaseUserS, PaginationQS
from errors import AlreadyExistsError, WasNotFoundError
from global_schemas import HTTPError

from flask_pydantic import validate

router = Blueprint(name='users', import_name=__name__, url_prefix='/api/v1/users')


@router.post('/')
@validate()
def add_user(body: CreateUserS):
    try:
        created_user = UserService.add(body)
        return created_user, 201

    except AlreadyExistsError as error:
        return HTTPError(message=str(error)), 409


@router.get('/')
@validate(response_many=True)
def get_users(query: PaginationQS):
    try:
        users = UserService.get_many(query.limit, query.page)
        return users

    except ValueError as error:
        return HTTPError(message=str(error)), 400


@router.get('/<user_id>')
@validate()
def get_user_by_id(user_id: int):
    user = UserService.get_one_by_id_or_none(user_id)
    if user is None:
        return HTTPError(message='User was not found.'), 404

    return user, 200


@router.put('/<user_id>')
@validate()
def update_user_by_id(user_id: int, body: BaseUserS):
    try:
        user = UserService.update_by_id(user_id, body)
        return user, 200

    except AlreadyExistsError as error:
        return HTTPError(message=str(error)), 409

    except WasNotFoundError as error:
        return HTTPError(message=str(error)), 404
