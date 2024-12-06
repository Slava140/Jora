from functools import wraps

from flask import jsonify, request
from pydantic import BaseModel


def validate():
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            annotations = func.__annotations__
            body_schema = annotations.get('body')

            if body_schema is not None:
                if issubclass(body_schema, BaseModel):
                    kwargs['body'] = body_schema(**request.json)
                else:
                    raise TypeError('body must be pydantic schema.')

            query_schema = annotations.get('query')
            if query_schema is not None:
                if issubclass(query_schema, BaseModel):
                    kwargs['query'] = query_schema(**request.args)
                else:
                    raise TypeError('query must be pydantic schema.')

            return func(*args, **kwargs)
        return wrapper
    return decorate
