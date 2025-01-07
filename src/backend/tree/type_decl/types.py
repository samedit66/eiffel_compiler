from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field

from tree.base import *


class TypeDecl(Node, ABC):
    pass


class IntegerType(TypeDecl):
    pass


class RealType(TypeDecl):
    pass


class BooleanType(TypeDecl):
    pass


class StringType(TypeDecl):
    pass


class CharacterType(TypeDecl):
    pass


class VoidType(TypeDecl):
    pass


@dataclass(match_args=True)
class ArrayType(TypeDecl):
    elements_type: TypeDecl


@dataclass(match_args=True)
class TupleType(TypeDecl):
    elements_type_list: list[TypeDecl] = field(default_factory=list)


@dataclass(match_args=True)
class ClassType(TypeDecl):
    type_name: str
    generics: list[TypeDecl] = field(default_factory=list)


@dataclass
class GenericType:
    template_type_name: str
    required_ancestor: TypeDecl | None = None


@dataclass
class LikeCurrentType(TypeDecl):
    pass


@dataclass
class LikeOtherFieldType(TypeDecl):
    other_field_name: str
