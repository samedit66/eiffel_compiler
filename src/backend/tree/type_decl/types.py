from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from ..base import *


class TypeDecl(Node, ABC):
    pass


@dataclass(match_args=True, kw_only=True)
class ClassType(TypeDecl):
    name: str
    generics: list[TypeDecl]


@dataclass(match_args=True, kw_only=True)
class TupleType(TypeDecl):
    generics: list[TypeDecl]


@dataclass(match_args=True, kw_only=True)
class GenericSpec(Node):
    template_type_name: str
    required_parent: TypeDecl | None = None


@dataclass
class LikeCurrent(TypeDecl):
    pass


@dataclass(match_args=True, kw_only=True)
class LikeFeature(TypeDecl):
    feature_name: str
