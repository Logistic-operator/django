from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IsochroneListRequest(_message.Message):
    __slots__ = ("warehouse_id",)
    WAREHOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    warehouse_id: int
    def __init__(self, warehouse_id: _Optional[int] = ...) -> None: ...

class IsochroneRetrieveRequest(_message.Message):
    __slots__ = ("warehouse_id", "timespan")
    WAREHOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESPAN_FIELD_NUMBER: _ClassVar[int]
    warehouse_id: int
    timespan: int
    def __init__(self, warehouse_id: _Optional[int] = ..., timespan: _Optional[int] = ...) -> None: ...

class Isochrone(_message.Message):
    __slots__ = ("id", "warehouse_id", "timespan", "all_geom")
    ID_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESPAN_FIELD_NUMBER: _ClassVar[int]
    ALL_GEOM_FIELD_NUMBER: _ClassVar[int]
    id: int
    warehouse_id: int
    timespan: int
    all_geom: str
    def __init__(self, id: _Optional[int] = ..., warehouse_id: _Optional[int] = ..., timespan: _Optional[int] = ..., all_geom: _Optional[str] = ...) -> None: ...
