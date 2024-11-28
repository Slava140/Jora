from flask import Flask

from api.v1.users.routes import router as users_router

app = Flask(__name__)
app.register_blueprint(users_router)


@app.route('/', methods=['GET'])
def ok():
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True, port=8000)
