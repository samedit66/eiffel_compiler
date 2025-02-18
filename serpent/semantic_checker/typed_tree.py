from __future__ import annotations
from dataclasses import dataclass, field

from serpent.tree.expr import Expr


@dataclass
class Type:
    name: str


@dataclass
class TypedExpr:
    kind: Type
    expr: Expr


@dataclass
class TypedIfExpr:
    condition: TypedExpr
    then_expr: TypedExpr
    else_expr: TypedExpr
    elseif_exprs: list[TypedElseIfExprBranch] = field(default_factory=list)


@dataclass
class TypedElseIfExprBranch:
    condition: TypedExpr
    expr: TypedExpr
