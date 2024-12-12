import random
import traceback
from pathlib import Path

from flask import Flask, jsonify, request, Response, Blueprint
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from pydantic import ValidationError

from api.v1.users.routes import router as users_router
from api.v1.projects.routes import router as projects_router
from api.v1.users.routes import auth_router

from config import settings
from database import db
from docs import Docs
from errors import AppError
from logger import get_logger

logger = get_logger('main')

STATIC_DIR = Path(__file__).parent.parent / 'static'

main_router = Blueprint(name='main', import_name=__name__, url_prefix='/')
main_router.register_blueprint(users_router)
main_router.register_blueprint(projects_router)
main_router.register_blueprint(auth_router)


@main_router.errorhandler(Exception)
def handle_all_errors(error: Exception):
    error_code = random.randint(100_000, 999_999)
    logger.error("[code:%d] %s", error_code, error)
    logger.debug("[code:%d] %s", error_code, traceback.format_exc())
    return jsonify({'message': f'Unknown error. Code: {error_code}'}), 500


@main_router.errorhandler(ValidationError)
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


@main_router.errorhandler(AppError)
def handle_app_error(error: AppError):
    logger.debug('App error: %s', error.message)
    return jsonify({'message': error.message}), error.status_code


@main_router.before_request
def log_before_request():
    view_func_name = request.url_rule.endpoint
    logger.info('Accepted by %s', view_func_name)


@main_router.after_request
def log_after_request(response: Response):
    view_func_name = request.url_rule.endpoint
    logger.info('Completed by %s (%d)', view_func_name, response.status_code)
    return response


@main_router.get('/')
def ok():
    return 'ok'


def create_app():
    app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url_psycopg
    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    app.register_blueprint(main_router)

    docs = Docs(title='Jora API', version='v1', app=app)
    docs.add_routes()
    docs.save(STATIC_DIR / 'docs.json')

    swagger_route = get_swaggerui_blueprint(base_url='/docs', api_url='/static/docs.json')
    app.register_blueprint(swagger_route)

    with app.app_context():
        db.init_app(app)

    return app


if __name__ == '__main__':
    logger.info('Start app...')
    try:
        app_ = create_app()
    except Exception as e:
        logger.error(str(e))
        logger.debug(traceback.format_exc())
        raise
    app_.run(debug=True, port=8000, host='0.0.0.0')
    logger.info('App is running')

