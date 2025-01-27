from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass


@dataclass(kw_only=True)
class Type:
    type_name: str

    def __eq__(self, other: Type) -> bool:
        return self.type_name == other.type_name

    def __hash__(self) -> int:
        return hash(self.type_name)


class TypeHierarchy:
    
    def __init__(self) -> None:
        self.types: dict[Type, list[Type]] = defaultdict(list)

    def rememeber(self, child: Type, parent: Type) -> None:
        if parent not in self.types:
            self.types[child].append(parent)

    def conforms_to(self, child: Type, parent: Type) -> bool:
        if child not in self.types:
            raise ValueError(f"Child type {child} not in type hierarchy")

        parents = self.types[child]
        if parent in parents:
            return True
        
        return any(self.conforms_to(candidate, parent) for candidate in parents)


@dataclass(kw_only=True)
class FeatureScope:
    ...


class LocalsScope:
    ...
