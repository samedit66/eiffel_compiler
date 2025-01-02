from __future__ import annotations
from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    first_line: int
    first_column: int
    last_list: int
    last_column: int

    @classmethod
    def from_dict(cls, loc_dict: dict) -> Location:
        first_line = loc_dict["first_line"]
        first_column = loc_dict["first_column"]
        last_line = loc_dict["last_line"]
        last_column = loc_dict["last_column"]
        return cls(first_line, first_column, last_line, last_column)


@dataclass
class Node(ABC):
    location: Location 


type IdentifierList = list[str]


def is_empty_node(node_dict: dict) -> bool:
    return node_dict["type"] == "empty"


class UnknownNodeTypeError(ValueError):
    pass
