from __future__ import annotations
from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    """Описывает положения узла синтакисического дерева в исходном тексте программы"""
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


@dataclass(match_args=True, kw_only=True)
class Node(ABC):
    """Абстрактный узел синтаксического дерева"""
    location: Location | None
    """Положение узла в тексте программы. Может быть None в ситуации, если
    одни узлы трансформируются в другие в процессе обработки дерева
    """


type Identifier = str
type IdentifierList = list[Identifier]


def is_empty_node(node_dict: dict) -> bool:
    return node_dict["type"] == "empty"


class UnknownNodeTypeError(ValueError):
    pass
