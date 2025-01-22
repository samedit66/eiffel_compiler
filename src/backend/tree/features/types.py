from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field

from ..base import *
from ..type_decl import TypeDecl
from ..stmts import Statement
from ..expr import Expr


@dataclass(match_args=True, kw_only=True)
class Feature(Node, ABC):
    name: Identifier
    clients: list[Identifier]


@dataclass(match_args=True, kw_only=True)
class Field(Feature):
    value_type: TypeDecl


@dataclass(match_args=True, kw_only=True)
class Constant(Feature):
    value_type: TypeDecl
    constant_value: Expr


@dataclass(match_args=True, kw_only=True)
class Parameter(Node):
    name: Identifier
    parameter_type: TypeDecl


@dataclass(match_args=True, kw_only=True)
class LocalVarDecl(Node):
    name: Identifier
    value_type: TypeDecl


@dataclass(match_args=True, kw_only=True)
class Condition(Node):
    condition_expr: Expr
    tag: Identifier | None = None


@dataclass(match_args=True, kw_only=True)
class Method(Feature):
    is_deferred: bool
    return_type: TypeDecl
    parameters: list[Parameter] = field(default_factory=list)
    do: list[Statement] = field(default_factory=list)
    local_var_decls: list[LocalVarDecl] = field(default_factory=list)
    require: list[Condition] = field(default_factory=list)
    ensure: list[Condition] = field(default_factory=list)


@dataclass(match_args=True, kw_only=True)
class ExternalMethod(Feature):
    language: str
