from typing import Any, Protocol


class _RespBase(Protocol):
    def __class_getitem__(cls, item: Any) -> Any:
        return Any


Resp = _RespBase
