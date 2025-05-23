from flask import jsonify
from flask_jwt_extended import set_access_cookies
from flask_openapi3 import APIBlueprint, Tag
from flask_security import permissions_accepted

from api.v1.users.services import UserService
from api.v1.users.schemas import CreateUserS, BaseUserS, ReadUserS, LoginS, LoggedInS, UserPath
from errors import WasNotFoundError
from global_schemas import PaginationQS, ErrorS
from global_schemas import security_schemas
from security import jwt_required


users_router = APIBlueprint(
    name='users', import_name=__name__, url_prefix='/api/v1/users',
    abp_security=security_schemas, abp_tags=[Tag(name='Users')],
    abp_responses={401: ErrorS, 403: ErrorS}
)
auth_router = APIBlueprint(
    name='auth', import_name=__name__, url_prefix='/auth',
    abp_tags=[Tag(name='Auth')],
)


@users_router.post('/', responses={201: ReadUserS, 409: ErrorS})
@jwt_required()
@permissions_accepted('user-write')
def add_user(body: CreateUserS):
    created_user = UserService.add(body)
    return jsonify(created_user.model_dump()), 201


@users_router.get('/', responses={200: ReadUserS, 400: ErrorS})
@jwt_required()
@permissions_accepted('user-read')
def get_users(query: PaginationQS):
    users = UserService.get_many(query.limit, query.page)
    return jsonify([user.model_dump() for user in users]), 200


@users_router.get('/<int:user_id>/', responses={200: ReadUserS, 404: ErrorS})
@jwt_required()
@permissions_accepted('user-read')
def get_user_by_id(path: UserPath):
    user = UserService.get_one_by_id_or_none(path.user_id)
    if user is None:
        raise WasNotFoundError(f'User with id {path.user_id}')

    return jsonify(user.model_dump()), 200


@users_router.put('/<int:user_id>/', responses={200: ReadUserS, 404: ErrorS, 409: ErrorS})
@jwt_required()
@permissions_accepted('user-write')
def update_user_by_id(path: UserPath, body: BaseUserS):
    updated_user_schema = UserService.update_by_id(path.user_id, body)
    return jsonify(updated_user_schema.model_dump()), 200


@users_router.delete('/<int:user_id>/', responses={204: None})
@jwt_required()
@permissions_accepted('user-write')
def delete_user_by_id(path: UserPath):
    UserService.delete_by_id(path.user_id)
    return jsonify(), 204


@auth_router.post('/login/', responses={200: LoggedInS, 401: ErrorS})
def login(body: LoginS):
    logged_in_user = UserService.login(body)
    response = jsonify(logged_in_user.model_dump())
    set_access_cookies(response, logged_in_user.access_token)
    return response, 200


@auth_router.post('/signup/', responses={201: LoggedInS, 409: ErrorS})
def signup(body: CreateUserS):
    logged_in_user = UserService.signup(body)
    response = jsonify(logged_in_user.model_dump())
    set_access_cookies(response, logged_in_user.access_token)
    return response, 201
