import typing
from pathlib import Path
from typing import Literal, Sequence, Type

from flask import Flask
from pydantic import BaseModel

from openapi_pydantic.v3.v3_0 import OpenAPI
from openapi_pydantic.v3.v3_0.util import PydanticSchema, construct_open_api_with_schema_class

from _types import Resp


class Docs:
    def __init__(self,
                 title: str,
                 version: str,
                 app: Flask,
                 methods_to_show: tuple[str] = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')):
        self.title = title
        self.version = version
        self.app = app
        self.methods_to_show = methods_to_show
        self.pytypes_to_jsontypes = {
            str: 'string',
            float: 'number',
            int: 'integer',
            bool: 'boolean',
            tuple: 'array',
            list: 'array',
            dict: 'object'
        }

        self.paths: dict[str, dict] = {}

    @staticmethod
    def __prepare_path(path: str):
        stripped_path = path.strip('/')
        result = []
        for part in stripped_path.split('/'):
            if part.startswith('<') and part.endswith('>'):
                part_without_brackets = part.strip('<>')
                *_, name = part_without_brackets.split(':')
                result.append('{' + name + '}')
            else:
                result.append(part)

        return '/' + '/'.join(result)

    def add_route(self,
                  method: Literal['get', 'post', 'put', 'patch', 'delete'],
                  path: str, description: str,
                  responses: Sequence[Resp] | None = None,
                  query_schema: Type[BaseModel] | None = None,
                  body_schema: Type[BaseModel] | None = None,
                  arguments: dict[str, typing.Any | None] | None = None
                  ):

        query_parameters = [
            {'name': name, 'in': 'query', 'style': 'path', 'schema': body}
            for name, body in query_schema.model_json_schema()['properties'].items()
        ] if query_schema is not None else []

        if arguments is not None:
            for name, type_ in arguments.items():
                schema = {'type': self.pytypes_to_jsontypes.get(type_)} if type_ is not None else {}
                parameter = {
                    'name': name,
                    'in': 'path',
                    'required': True,
                    'schema': schema
                }
                query_parameters.append(parameter)

        request_body = {
            'content': {
                'application/json': {
                    'media_type_schema': PydanticSchema(schema_class=body_schema)
                }
            }
        } if body_schema is not None else None

        responses = {
            str(status_code): {
                'description': description,
                'content': {
                    'application/json': {
                        'media_type_schema': PydanticSchema(schema_class=pydantic_model)
                    }
                }
            }
            for pydantic_model, status_code in responses
        } if responses is not None else {}

        path_item = {
            method: {
                'parameters': query_parameters,
                'requestBody': request_body,
                'responses': responses
            }
        }

        if self.paths.get(path) is None:
            self.paths[path] = path_item
        else:
            self.paths.get(path).update(path_item)

    def add_routes(self):
        path_func_dict = self.app.view_functions
        for rule in self.app.url_map.iter_rules():
            path = self.__prepare_path(rule.rule)
            methods = [method.lower() for method in rule.methods & set(self.methods_to_show)]

            annotations: dict = path_func_dict[rule.endpoint].__annotations__

            returns = typing.get_args(annotations.get('return'))
            responses = []
            if returns:
                if isinstance(BaseModel, type(returns[0])):
                    responses.append(returns)
                else:
                    responses += [typing.get_args(response) for response in returns]
            query_schema = annotations.get('query')
            body_schema = annotations.get('body')
            arguments = {name: annotations.get(name) for name in rule.arguments}

            for method in methods:
                self.add_route(
                    method=method, path=path, description=rule.endpoint,
                    query_schema=query_schema, body_schema=body_schema,
                    responses=responses, arguments=arguments
                )

    def get_docs_json(self, indent: int = 2):
        open_api = OpenAPI(**{
            'info': {'title': self.title, 'version': self.version},
            'paths': self.paths
        })
        open_api = construct_open_api_with_schema_class(open_api)
        return open_api.model_dump_json(by_alias=True, exclude_none=True, indent=indent)

    def save(self, filename: Path = Path('docs.json')):
        if filename.is_dir():
            filename = filename / 'docs.json'

        elif filename.is_file() and not str(filename).endswith('.json'):
            filename = f'{filename}.json'

        with open(filename, 'w', encoding='utf-8') as json_file:
            json_file.write(self.get_docs_json())
