from flask import jsonify
from flask_jwt_extended import set_access_cookies
from flask_openapi3 import APIBlueprint
from flask_security import roles_accepted, current_user

from api.v1.users.services import UserService
from api.v1.users.schemas import CreateUserS, BaseUserS, ReadUserS, LoginS, LoggedInS, UserPath
from app import app
from database import db
from errors import WasNotFoundError
from global_schemas import PaginationQS
from global_schemas import security_schemas
from security import jwt_required

users_router = APIBlueprint(name='users', import_name=__name__, url_prefix='/api/v1/users', abp_security=security_schemas)
auth_router = APIBlueprint(name='auth', import_name=__name__, url_prefix='/auth')


@users_router.post('/')
@jwt_required()
@roles_accepted('admin')
def add_user(body: CreateUserS):
    created_user = UserService.add(body)
    return jsonify(created_user.model_dump()), 201


@users_router.get('/')
@jwt_required()
@roles_accepted('admin')
def get_users(query: PaginationQS):
    users = UserService.get_many(query.limit, query.page)
    return jsonify([user.model_dump() for user in users]), 200


@users_router.get('/<int:user_id>/')
@jwt_required()
@roles_accepted('admin')
def get_user_by_id(path: UserPath):
    user = UserService.get_one_by_id_or_none(path.user_id)
    if user is None:
        raise WasNotFoundError(f'User with id {path.user_id}')

    return jsonify(user.model_dump()), 200


@users_router.put('/')
@jwt_required()
@roles_accepted('admin', 'user')
def update_user_by_id(body: BaseUserS):
    updated_user_schema = UserService.update_by_id(current_user.id, body)
    return jsonify(updated_user_schema.model_dump()), 200


@users_router.delete('/')
@jwt_required()
@roles_accepted('admin', 'user')
def delete_user_by_id():
    UserService.delete_by_id(current_user.id)
    return jsonify(), 204


@auth_router.post('/login/')
def login(body: LoginS):
    logged_in_user = UserService.login(body)
    response = jsonify(logged_in_user.model_dump())
    set_access_cookies(response, logged_in_user.access_token)
    return response, 200


@auth_router.post('/signup/')
def signup(body: CreateUserS):
    logged_in_user = UserService.signup(body)
    response = jsonify(logged_in_user.model_dump())
    set_access_cookies(response, logged_in_user.access_token)
    return response, 201
