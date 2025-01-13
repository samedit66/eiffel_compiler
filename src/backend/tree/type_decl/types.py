from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from ..base import *


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


@dataclass(match_args=True, kw_only=True)
class ArrayType(TypeDecl):
    elements_type: TypeDecl


@dataclass(match_args=True, kw_only=True)
class TupleType(TypeDecl):
    elements_type_list: list[TypeDecl]


@dataclass(match_args=True, kw_only=True)
class ClassType(TypeDecl):
    type_name: str
    generics: list[TypeDecl]


@dataclass(match_args=True, kw_only=True)
class GenericType(Node):
    template_type_name: str
    required_parent: TypeDecl | None = None


@dataclass
class LikeCurrentType(TypeDecl):
    pass


@dataclass(match_args=True, kw_only=True)
class LikeOtherFieldType(TypeDecl):
    other_field_name: str
