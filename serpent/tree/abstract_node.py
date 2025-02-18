from __future__ import annotations
from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    first_line: int
    first_column: int
    last_line: int
    last_column: int
    filename: str | None

    def __repr__(self) -> str:
        filename = self.filename or "<input>"
        if (self.first_line == self.last_line and
                self.first_column == self.last_column):
            return f"{filename}@{self.first_line}:{self.first_column}"
        else:
            return f"{filename}@{self.first_line}:{self.first_column}-" \
                f"{self.last_line}:{self.last_column}"


@dataclass(kw_only=True)
class Node(ABC):
    location: Location | None


class UnknownNodeTypeError(ValueError):
    pass
