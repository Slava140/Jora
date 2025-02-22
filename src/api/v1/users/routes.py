from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_openapi3 import APIBlueprint

from api.v1.users.services import UserService
from api.v1.users.schemas import CreateUserS, BaseUserS, ReadUserS, LoginS, LoggedInS
from errors import WasNotFoundError
from global_schemas import PaginationQS
from security import security

users_router = APIBlueprint(name='users', import_name=__name__, url_prefix='/api/v1/users', abp_security=security)
auth_router = APIBlueprint(name='auth', import_name=__name__, url_prefix='/auth')


@users_router.post('/')
@jwt_required()
def add_user(body: CreateUserS):
    created_user = UserService.add(body)
    return jsonify(created_user.model_dump()), 201


@users_router.get('/')
@jwt_required()
def get_users(query: PaginationQS):
    users = UserService.get_many(query.limit, query.page)
    return jsonify([user.model_dump() for user in users]), 200


@users_router.get('/<int:user_id>/')
@jwt_required()
def get_user_by_id(user_id: int):
    user = UserService.get_one_by_id_or_none(user_id)
    if user is None:
        raise WasNotFoundError(f'User with id {user_id}')

    return jsonify(user.model_dump()), 200


@users_router.put('/<int:user_id>/')
@jwt_required()
def update_user_by_id(user_id: int, body: BaseUserS):
    user = UserService.update_by_id(user_id, body)
    return jsonify(user.model_dump()), 200


@users_router.delete('/<int:user_id>/')
@jwt_required()
def delete_user_by_id(user_id: int):
    UserService.delete_by_id(user_id)
    return jsonify(), 204


@auth_router.post('/login/')
def login(body: LoginS):
    logged_in_user = UserService.login(body)
    return jsonify(logged_in_user.model_dump()), 200


@auth_router.post('/signup/')
def signup(body: CreateUserS):
    logged_in_user = UserService.signup(body)
    return jsonify(logged_in_user.model_dump()), 201
