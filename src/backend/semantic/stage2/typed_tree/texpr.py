from __future__ import annotations
from dataclasses import dataclass, field

from .tables import Type


@dataclass(kw_only=True)
class TypedExpr:
    type_of: Type


@dataclass(kw_only=True)
class TypedInteger(TypedExpr):
    value: int


@dataclass(kw_only=True)
class TypedReal(TypedExpr):
    value: float


@dataclass(kw_only=True)
class TypedCharacter(TypedExpr):
    value: str


@dataclass(kw_only=True)
class TypedString(TypedExpr):
    value: str


@dataclass(kw_only=True)
class TypedBool(TypedExpr):
    value: bool


@dataclass(kw_only=True)
class TypedVoid(TypedExpr):
    pass


@dataclass(kw_only=True)
class TypedCurrent(TypedExpr):
    pass


@dataclass(kw_only=True)
class TypedResult(TypedExpr):
    pass


@dataclass(kw_only=True)
class TypedTupleLiteral(TypedExpr):
    values: list[TypedExpr] = field(default_factory=list)


@dataclass(kw_only=True)
class TypedArrayLiteral(TypedExpr):
    values: list[TypedExpr] = field(default_factory=list)


@dataclass(kw_only=True)
class TypedFeatureCall(TypedExpr):
    name: str
    arguments: list[TypedExpr] = field(default_factory=list)
    owner: Type


@dataclass(kw_only=True)
class TypedPrecursorCall(TypedExpr):
    feature_name: str
    parent: Type
    arguments: list[TypedExpr] = field(default_factory=list)


@dataclass(kw_only=True)
class TypedCreateExpr(TypedExpr):
    constructor_call: TypedFeatureCall


@dataclass(kw_only=True)
class TypedElseifExprBranch(TypedExpr):
    condition: TypedExpr
    expr: TypedExpr


@dataclass(kw_only=True)
class TypedIfExpr(TypedExpr):
    condition: TypedExpr
    then_expr: TypedExpr
    else_expr: TypedExpr
    elseif_exprs: list[TypedExpr] = field(default_factory=list)


@dataclass(kw_only=True)
class TypedBracketAccess(TypedExpr):
    indexed_expr: TypedExpr
    indices: list[TypedExpr]

