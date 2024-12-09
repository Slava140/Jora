from pathlib import Path

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from pydantic import ValidationError

from api.v1.users.routes import router as users_router
from api.v1.projects.routes import router as projects_router
from api.v1.users.routes import auth_router

from config import settings
from docs import Docs
from errors import AppError

STATIC_DIR = Path(__file__).parent.parent / 'static'

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET
app.config['JWT_TOKEN_LOCATION'] = ['headers']


app.register_blueprint(users_router)
app.register_blueprint(projects_router)
app.register_blueprint(auth_router)

docs = Docs(title='Jora API', version='v1', app=app)
docs.add_routes()
docs.save(STATIC_DIR / 'docs.json')

swagger_route = get_swaggerui_blueprint(base_url='/docs', api_url='/static/docs.json')
app.register_blueprint(swagger_route)

jwt = JWTManager(app)


@app.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    return jsonify([
        {
            'loc': e['loc'],
            'input': e['input'],
            'msg': e['msg']
        } for e in error.errors()
    ]), 422


@app.errorhandler(AppError)
def handle_app_error(error: AppError):
    return jsonify({'message': error.message}), error.status_code


@app.route('/', methods=['GET'])
def ok():
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
