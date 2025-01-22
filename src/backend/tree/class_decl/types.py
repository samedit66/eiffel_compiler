from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

from ..base import *
from ..features import Feature
from ..type_decl import GenericType


@dataclass(match_args=True, kw_only=True)
class Alias(Node):
    original_name: Identifier
    alias_name: Identifier

    def __hash__(self) -> int:
        return hash(self.original_name)


@dataclass(match_args=True, kw_only=True)
class Parent(Node):
    class_name: Identifier
    generics: list[GenericType] = field(default_factory=list)
    rename: list[Alias] = field(default_factory=list)
    undefine: list[Identifier] = field(default_factory=list)
    redefine: list[Identifier] = field(default_factory=list)
    select: list[Identifier] = field(default_factory=list)
    class_decl: ClassDecl | None = None

    def __hash__(self) -> int:
        return hash(self.class_name)


@dataclass(match_args=True, kw_only=True)
class ClassDecl(Node):
    class_name: Identifier
    is_deferred: bool
    generics: list[GenericType]
    inherit: list[Parent]
    create: list[Identifier]
    features: list[Feature]
    defined_in_file: Path | None

    def __hash__(self) -> int:
        return hash(self.class_name)
    