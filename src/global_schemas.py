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


class ErrorS(BaseModel):
    message: str


class ValidationErrorS(BaseModel):
    type:  str
    loc:   list[str]
    msg:   str
    input: dict