from copy import deepcopy
from datetime import datetime
from typing import Annotated
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, registry, mapped_column


sql_utc_now = text("timezone('utc', now())")

str_255 = Annotated[str, 255]
str_500 = Annotated[str, 500]

str_255_unique = Annotated[str, mapped_column(String(255), unique=True)]

pk_int = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
pk_uuid = Annotated[UUID, mapped_column(primary_key=True)]

created_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=sql_utc_now)]
updated_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=sql_utc_now, onupdate=sql_utc_now)]


fk_user_id = Annotated[int, mapped_column(ForeignKey(column='users.id', ondelete='CASCADE'))]
fk_task_id = Annotated[int, mapped_column(ForeignKey(column='tasks.id'))]
#
# datetime_utc_tz = Annotated[datetime, mapped_column(DateTime(timezone=True))]


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


db = SQLAlchemy(model_class=Base, engine_options={"connect_args": {"options": "-c timezone=utc"}})
