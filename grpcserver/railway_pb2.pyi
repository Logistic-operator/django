from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RailwayListRequest(_message.Message):
    __slots__ = ("is_cont",)
    IS_CONT_FIELD_NUMBER: _ClassVar[int]
    is_cont: bool
    def __init__(self, is_cont: bool = ...) -> None: ...

class NeighborhoodListRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NeighborhoodOpListRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RailwayRetrieveRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class NeighborhoodRetrieveRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class NeighborhoodOpRetrieveRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class OptimizeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Railway(_message.Message):
    __slots__ = ("id", "iid", "point", "is_cont")
    ID_FIELD_NUMBER: _ClassVar[int]
    IID_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    IS_CONT_FIELD_NUMBER: _ClassVar[int]
    id: int
    iid: int
    point: str
    is_cont: bool
    def __init__(self, id: _Optional[int] = ..., iid: _Optional[int] = ..., point: _Optional[str] = ..., is_cont: bool = ...) -> None: ...

class Neighborhood(_message.Message):
    __slots__ = ("id", "source_id", "target_id", "length")
    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    id: int
    source_id: int
    target_id: int
    length: float
    def __init__(self, id: _Optional[int] = ..., source_id: _Optional[int] = ..., target_id: _Optional[int] = ..., length: _Optional[float] = ...) -> None: ...

class NeighborhoodOp(_message.Message):
    __slots__ = ("id", "source_id", "target_id", "length")
    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    id: int
    source_id: int
    target_id: int
    length: float
    def __init__(self, id: _Optional[int] = ..., source_id: _Optional[int] = ..., target_id: _Optional[int] = ..., length: _Optional[float] = ...) -> None: ...

class Optimized(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...
