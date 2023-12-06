from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ActionType(Enum):
    query = 1
    memorize = 2
    unknown = 3


@dataclass
class Collection:
    title: str
    abstract: str
    keywords: List[str]
    metadata: Optional[dict] = None
