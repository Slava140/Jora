from pathlib import Path

from flask_jwt_extended import JWTManager
from flask_openapi3 import OpenAPI, Info

from config import settings
from database import db
from global_schemas import jwt_schema


STATIC_DIR = Path(__file__).parent.parent / 'static'
STATIC_DIR.mkdir(exist_ok=True)


api_info = Info(title="Jora API", version="1.0.0")

app = OpenAPI(
    __name__,
    info=api_info, security_schemes={"jwt": jwt_schema},
    static_folder=STATIC_DIR, static_url_path='/static'
)

app.config['SECRET_KEY'] = settings.JWT_SECRET
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url_psycopg
app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.access_token_ttl_timedelta
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

with app.app_context():
    db.init_app(app)

JWTManager(app)