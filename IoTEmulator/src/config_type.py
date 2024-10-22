import operator
from typing import TypedDict, Union, Literal, Dict, Optional, Tuple, List


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


class InstructionType(TypedDict):
    device: Tuple[str, int]
    name: str
    operator: Literal["==", "!=", "<", "<=", ">", ">="]
    value: Union[bool, float]


class ActionType(TypedDict):
    name: str
    value: Union[bool, float]


class ControlConfig(TypedDict):
    id: Optional[str]
    match: Literal["all", "any"]
    instructions: List[InstructionType]
    actions: List[ActionType]


operators_dict = {
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge
}
