from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Union


class ActionStatusCode(int, Enum):
    ING = 0
    SUCCESS = 1
    FAILED = -1


class ActionValidCode(int, Enum):
    FINISH = 1
    OPEN = 0
    CLOSED = -1
    INVALID = -2
    ABSENT = -3  # NO ACTION


@dataclass
class ActionReturn:
    args: Dict
    url: Optional[str] = None
    type: Optional[str] = None
    result: Optional[str] = None
    errmsg: Optional[str] = None
    state: Union[ActionStatusCode, int] = ActionStatusCode.SUCCESS
    thought: Optional[str] = None
    valid: Optional[ActionValidCode] = ActionValidCode.OPEN

