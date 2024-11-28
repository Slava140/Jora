from fastapi import APIRouter
from sqlalchemy.orm import Session

from api.v1.users.services import UserService
from api.v1.users.schemas import UserWithPlainPassS
from dependencies import dbDep

router = APIRouter(prefix='/api/v1/users')


@router.post('/')
def add_user(session: dbDep, user: UserWithPlainPassS):
    return UserService().add(session, user)
