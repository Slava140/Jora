from pydantic import BaseModel, PositiveInt

jwt_schema = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
}

security_schemas = [
    {'jwt': []}
]


class PaginationQS(BaseModel):
    page:   PositiveInt = 1
    limit:  PositiveInt = 10
