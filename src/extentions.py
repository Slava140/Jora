from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_dramatiq import Dramatiq
from flask_jwt_extended import JWTManager
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

from database import Base

db = SQLAlchemy(
    model_class=Base,
    engine_options={
        "connect_args":{"options": "-c timezone=utc"}
    },
    session_options={'expire_on_commit': True, 'autobegin': True}
)
scheduler = APScheduler()
dramatiq = Dramatiq()
jwt_manager = JWTManager()
cors = CORS()
security = Security()