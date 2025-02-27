import random
import traceback

import werkzeug.exceptions
from flask import jsonify, request, Response
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError
from pydantic import ValidationError

from api.v1.users.routes import auth_router, users_router
from api.v1.projects.routes import projects_router, tasks_router, comments_router
from media.routes import router as media_router

from errors import AppError
from logger import get_logger
from app import app

logger = get_logger('main')


app.register_api(auth_router)
app.register_api(users_router)
app.register_api(projects_router)
app.register_api(tasks_router)
app.register_api(comments_router)
app.register_api(media_router)


@app.errorhandler(Exception)
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


@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_flask_http_error(error: werkzeug.exceptions.HTTPException):
    """ Ловит ошибки генерируемые Flask-ом """
    return jsonify({'message': error.description}), error.code


@app.errorhandler(ValidationError)
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


@app.errorhandler(JWTExtendedException)
def handle_flask_jwt_error(error: JWTExtendedException):
    logger.debug('JWT error %s', traceback.format_exc())
    return jsonify({'message': str(error)}), 401


@app.errorhandler(PyJWTError)
def handle_jwt_error(error: PyJWTError):
    logger.debug('JWT error %s', traceback.format_exc())
    return jsonify({'message': str(error)}), 401


@app.errorhandler(AppError)
def handle_app_error(error: AppError):
    """ Ловит все ошибки генерируемые приложением """
    logger.debug('App error: %s', error.message)
    return jsonify({'message': error.message}), error.status_code


@app.before_request
def log_before_request():
    view_func_name = request.url_rule.endpoint
    logger.info('Accepted by %s', view_func_name)


@app.after_request
def log_after_request(response: Response):
    view_func_name = request.url_rule.endpoint
    logger.info('Completed by %s (%d)', view_func_name, response.status_code)
    return response


@app.get('/')
def ok():
    return 'ok'


if __name__ == '__main__':
    logger.info('Start app...')
    try:
        app.run(debug=True, port=8000, host='0.0.0.0')
        logger.info('App is running')
    except Exception as e:
        logger.error(str(e))
        logger.debug(traceback.format_exc())
        raise
