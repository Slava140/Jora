from fastapi import FastAPI

from api.v1.users.routes import router as users_router

app = FastAPI()
app.include_router(users_router, tags=['Users'])


@app.get('/')
def ok():
    return 'ok'
