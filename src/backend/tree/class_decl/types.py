from __future__ import annotations
from dataclasses import dataclass
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
    generics: list[GenericType]
    rename: list[Alias]
    undefine: list[Identifier]
    redefine: list[Identifier]
    select: list[Identifier]


@dataclass(match_args=True, kw_only=True)
class ClassDecl(Node):
    class_name: Identifier
    is_deferred: bool
    generics: list[GenericType]
    inherit: list[Parent]
    create: list[Identifier]
    features: list[Feature]
    defined_in_file: Path | None
