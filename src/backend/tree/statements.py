from __future__ import annotations
from dataclasses import (
    dataclass,
    field,
)


@dataclass
class StatementList:
    
    @classmethod
    def from_list(cls, statement_list: list) -> StatementList:
        return cls()

