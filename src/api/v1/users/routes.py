from flask import Blueprint, request, jsonify

from api.v1.users.services import UserService
from api.v1.users.schemas import CreateUserS
from errors import AlreadyExistsError
from global_schemas import HTTPError

router = Blueprint(name='users', import_name=__name__, url_prefix='/api/v1/users')


@router.post('/')
def add_user():
    user = CreateUserS(**request.json)
    try:
        created_user = UserService.add(user)
        return jsonify(created_user.model_dump()), 201
    except AlreadyExistsError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 409


@router.get('/')
def get_users():
    limit_arg = request.args.get('limit', default=10, type=int)
    page_arg = request.args.get('page', default=1, type=int)
    try:
        users = UserService.get_many(limit_arg, page_arg)
        return jsonify([user.model_dump() for user in users]), 200
    except ValueError as error:
        return jsonify(HTTPError(message=str(error)).model_dump()), 400


@router.get('/<int:user_id>')
def get_user_by_id(user_id: int):
    user = UserService.get_one_by_id_or_none(user_id)
    if user is None:
        return jsonify(HTTPError(message='User was not found.').model_dump()), 404

    return jsonify(user.model_dump()), 200
