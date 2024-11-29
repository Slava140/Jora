from pathlib import Path

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from api.v1.users.routes import router as users_router

app = Flask(__name__, static_folder=Path(__file__).parent.parent / 'static', static_url_path='/static')

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swagger_route = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
       'app_name': 'My App'
    }
)

app.register_blueprint(swagger_route)
app.register_blueprint(users_router)


@app.route('/', methods=['GET'])
def ok():
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True, port=8000)
