from pydantic import BaseModel, PositiveInt

class PaginationQS(BaseModel):
    page:           PositiveInt = 1
    limit:          PositiveInt = 10
