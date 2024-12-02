from pathlib import Path

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from api.v1.users.routes import router as users_router
from docs import Docs

STATIC_DIR = Path(__file__).parent.parent / 'static'

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
app.register_blueprint(users_router)

docs = Docs(title='Jora API', version='v1', app=app)
docs.add_routes()
docs.save(STATIC_DIR / 'docs.json')


swagger_route = get_swaggerui_blueprint(base_url='/docs', api_url='/static/docs.json')
app.register_blueprint(swagger_route)


@app.route('/', methods=['GET'])
def ok():
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True, port=8000)
