from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

from tree.base import *
from tree.features import Feature
from tree.type_decl import GenericType


@dataclass(match_args=True, kw_only=True)
class Alias(Node):
    original_name: Identifier
    alias_name: Identifier


@dataclass(match_args=True, kw_only=True)
class Parent(Node):
    class_name: Identifier
    generics: list[GenericType] = field(default_factory=list)
    rename: list[Alias] = field(default_factory=list)
    undefine: list[Identifier] = field(default_factory=list)
    redefine: list[Identifier] = field(default_factory=list)
    select: list[Identifier] = field(default_factory=list)


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
    