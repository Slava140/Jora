from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from api.v1.users.services import UserService
from api.v1.users.schemas import CreateUserS

router = Blueprint(name='users', import_name=__name__, url_prefix='/api/v1/users')


@router.route(rule='/', methods=['POST'])
def add_user():
    user = CreateUserS(**request.json)
    UserService().add(user)
    return jsonify(user.model_dump())
