from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from tree.base import *
from tree.type_decl import TypeDecl
from tree.stmts import Statement
from tree.expr import Expr


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
    parameters: list[Parameter]
    do: list[Statement]
    local_var_decls: list[LocalVarDecl]
    require: list[Condition]
    ensure: list[Condition]
