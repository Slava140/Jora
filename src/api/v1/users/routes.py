from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from api.v1.users.services import UserService
from api.v1.users.schemas import CreateUserS
from errors import AlreadyExistsError

router = Blueprint(name='users', import_name=__name__, url_prefix='/api/v1/users')


@router.route(rule='/', methods=['POST'])
def add_user():
    user = CreateUserS(**request.json)
    try:
        created_user = UserService.add(user)
        return jsonify(created_user.model_dump()), 201
    except AlreadyExistsError as error:
        return jsonify({'message': str(error)}), 409


@router.route(rule='/', methods=['GET'])
def get_users():
    limit_arg = request.args.get('limit', default=10, type=int)
    page_arg = request.args.get('page', default=1, type=int)
    try:
        users = UserService.get_many(limit_arg, page_arg)
        return jsonify([user.model_dump() for user in users]), 200
    except ValueError as error:
        return jsonify({'message': str(error)}), 400
