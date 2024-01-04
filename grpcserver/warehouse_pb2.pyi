from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Warehouse(_message.Message):
    __slots__ = ("id", "phone", "point", "nearest_railway_id", "nearest_railway_length")
    ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    NEAREST_RAILWAY_ID_FIELD_NUMBER: _ClassVar[int]
    NEAREST_RAILWAY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    id: int
    phone: str
    point: str
    nearest_railway_id: int
    nearest_railway_length: float
    def __init__(self, id: _Optional[int] = ..., phone: _Optional[str] = ..., point: _Optional[str] = ..., nearest_railway_id: _Optional[int] = ..., nearest_railway_length: _Optional[float] = ...) -> None: ...

class WarehouseListRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WarehouseRetrieveRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class WarehouseIsoRequest(_message.Message):
    __slots__ = ("id", "timespans")
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESPANS_FIELD_NUMBER: _ClassVar[int]
    id: int
    timespans: str
    def __init__(self, id: _Optional[int] = ..., timespans: _Optional[str] = ...) -> None: ...

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
