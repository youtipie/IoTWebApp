from typing import TypedDict, Union, Literal, Dict, Optional


class BoolType(TypedDict):
    type: Literal["bool"]
    default: Optional[bool]


class RangeType(TypedDict):
    type: Literal["range"]
    default: Optional[float]
    min: float
    max: float


DataType = Union[BoolType, RangeType]


class ConfigType(TypedDict):
    id: Optional[str]
    name: str
    description: Optional[str]
    readings: Optional[Dict[str, DataType]]
    parameters: Optional[Dict[str, DataType]]
    def validate(self) -> None:
        pass