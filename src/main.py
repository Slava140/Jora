import random
import traceback
from pathlib import Path

import werkzeug.exceptions
from flask import jsonify, request, Response
from flask_openapi3 import OpenAPI, Info, APIBlueprint
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_security import SQLAlchemyUserDatastore, Security
from jwt.exceptions import PyJWTError
from pydantic import ValidationError

from api.v1.users.models import UserM, RoleM
from api.v1.users.routes import auth_router, users_router
from api.v1.projects.routes import projects_router, tasks_router, comments_router
from media.routes import router as media_router

from config import settings
from database import db
from errors import AppError
from logger import get_logger
from security import jwt_schema

logger = get_logger('main')

STATIC_DIR = Path(__file__).parent.parent / 'static'
STATIC_DIR.mkdir(exist_ok=True)

api = APIBlueprint(name='main', import_name=__name__, url_prefix='/')
api.register_api(auth_router)
api.register_api(users_router)
api.register_api(projects_router)
api.register_api(tasks_router)
api.register_api(comments_router)
api.register_api(media_router)



@api.errorhandler(Exception)
def handle_all_errors(error: Exception):
    """
    Ловит все ошибки.

    Возвращает пользователю код ошибки
    по которому можно найти полный traceback в логах.
    """
    error_code = random.randint(100_000, 999_999)
    logger.error("[code:%d] %s", error_code, error)
    logger.debug("[code:%d] %s", error_code, traceback.format_exc())
    return jsonify({'message': f'Unknown error. Code: {error_code}'}), 500


@api.errorhandler(werkzeug.exceptions.HTTPException)
def handle_flask_http_error(error: werkzeug.exceptions.HTTPException):
    """ Ловит ошибки генерируемые Flask-ом """
    return jsonify({'message': error.description}), error.code


@api.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    errors = [
        {
            'loc': err['loc'],
            'input': err['input'],
            'msg': err['msg']
        } for err in error.errors()
    ]
    logger.debug('Validation Error: %s', errors)
    return jsonify(errors), 422


@api.errorhandler(JWTExtendedException)
def handle_flask_jwt_error(error: JWTExtendedException):
    logger.debug('JWT error %s', traceback.format_exc())
    return jsonify({'message': str(error)}), 401


@api.errorhandler(PyJWTError)
def handle_jwt_error(error: PyJWTError):
    logger.debug('JWT error %s', traceback.format_exc())
    return jsonify({'message': str(error)}), 401


@api.errorhandler(AppError)
def handle_app_error(error: AppError):
    """ Ловит все ошибки генерируемые приложением """
    logger.debug('App error: %s', error.message)
    return jsonify({'message': error.message}), error.status_code


@api.before_request
def log_before_request():
    view_func_name = request.url_rule.endpoint
    logger.info('Accepted by %s', view_func_name)


@api.after_request
def log_after_request(response: Response):
    view_func_name = request.url_rule.endpoint
    logger.info('Completed by %s (%d)', view_func_name, response.status_code)
    return response


@api.get('/')
def ok():
    return 'ok'


def create_app():
    api_info = Info(title="Jora API", version="1.0.0")

    app = OpenAPI(
        __name__,
        info=api_info, security_schemes={"jwt": jwt_schema},
        static_folder=STATIC_DIR, static_url_path='/static'
    )

    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url_psycopg
    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.access_token_ttl_timedelta
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

    app.register_api(api)

    with app.app_context():
        db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, UserM, RoleM)
    security = Security(app, user_datastore)

    JWTManager(app)

    return app


if __name__ == '__main__':
    logger.info('Start app...')
    try:
        app_ = create_app()
        app_.run(debug=True, port=8000, host='0.0.0.0')
        logger.info('App is running')
    except Exception as e:
        logger.error(str(e))
        logger.debug(traceback.format_exc())
        raise
