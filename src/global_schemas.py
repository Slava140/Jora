from pydantic import BaseModel, PositiveInt


class HTTPError(BaseModel):
    message: str


class EmptyResponse(BaseModel):
    ...


class PaginationQS(BaseModel):
    page:   PositiveInt = 1
    limit:  PositiveInt = 10
