from copy import deepcopy
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, registry, mapped_column
from sqlalchemy.sql import expression

sql_utc_now = text("timezone('utc', now())")

str_255 = Annotated[str, 255]
str_500 = Annotated[str, 500]

str_255_unique = Annotated[str, mapped_column(String(255), unique=True)]

pk_int = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
pk_uuid = Annotated[UUID, mapped_column(primary_key=True)]

is_active = Annotated[bool, mapped_column(Boolean, server_default=expression.true())]
is_archived = Annotated[bool, mapped_column(Boolean, server_default=expression.false())]
task_status = Annotated[Literal['open', 'in_progress', 'finished'], mapped_column(String(50), server_default='open')]

created_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=sql_utc_now)]
updated_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=sql_utc_now, onupdate=sql_utc_now)]
datetime_utc_tz = Annotated[datetime, mapped_column(DateTime(timezone=True))]


fk_user_id = Annotated[int, mapped_column(ForeignKey(column='users.id'))]
fk_role_id = Annotated[int, mapped_column(ForeignKey(column='roles.id'))]
fk_project_id = Annotated[int, mapped_column(ForeignKey(column='projects.id'))]
fk_task_id = Annotated[int, mapped_column(ForeignKey(column='tasks.id'))]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_255: String(255),
            str_500: String(500),
        }
    )

    def to_dict(self) -> dict:
        d = deepcopy(self.__dict__)
        d.pop('_sa_instance_state')
        return d


db = SQLAlchemy(
    model_class=Base,
    engine_options={
        "connect_args":{"options": "-c timezone=utc"}
    },
    session_options={'expire_on_commit': True, 'autobegin': True}
)
