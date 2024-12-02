from pydantic import BaseModel


class HTTPError(BaseModel):
    message: str


class EmptyResponse(BaseModel):
    ...
