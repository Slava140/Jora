from pathlib import Path

from flask import jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_openapi3 import OpenAPI, Info
from pydantic import ValidationError

from config import settings
from database import db
from global_schemas import jwt_schema, ErrorS, ValidationErrorS

STATIC_DIR = Path(__file__).parent.parent / 'static'
STATIC_DIR.mkdir(exist_ok=True)


api_info = Info(title="Jora API", version="1.0.0")


def validation_error_callback(error: ValidationError):
    response = make_response(error.json(include_url=False, include_context=False, indent=2))
    response.status_code = 422
    # response.headers["Content-Type"] = "application/json"
    # response.status_code = getattr(current_app, "validation_error_status", 422)
    return response


app = OpenAPI(
    __name__,
    info=api_info,
    security_schemes={"jwt": jwt_schema},
    validation_error_model=ValidationErrorS,
    validation_error_callback=validation_error_callback,
    static_folder=STATIC_DIR, static_url_path='/static'
)

app.config['SECRET_KEY'] = settings.JWT_SECRET
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url_psycopg
app.config["SQLALCHEMY_ECHO"] = False
app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.access_token_ttl_timedelta
app.config['JWT_TOKEN_LOCATION'] = ['headers']

with app.app_context():
    db.init_app(app)


JWTManager(app)