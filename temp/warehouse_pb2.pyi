from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Warehouse(_message.Message):
    __slots__ = ("id", "phone", "point")
    ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    id: int
    phone: str
    point: str
    def __init__(self, id: _Optional[int] = ..., phone: _Optional[str] = ..., point: _Optional[str] = ...) -> None: ...

class WarehouseListRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
