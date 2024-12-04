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

            result = func(*args, **kwargs)

            if isinstance(result, BaseModel):
                return jsonify(result.model_dump()), 200

            elif type(result) is tuple and len(result) >= 2:
                if isinstance(result[0], BaseModel) and type(result[1]) is int:
                    schema, status_code = result
                    return jsonify(schema.model_dump()), status_code
                elif isinstance(result[0], tuple) and type(result[1]) is int:
                    schemas, status_code = result
                    return jsonify([schema.model_dump() for schema in schemas]), status_code
                else:
                    schemas, status_code = result, 200
                    return jsonify([schema.model_dump() for schema in schemas]), status_code
            else:
                return result
        return wrapper
    return decorate
