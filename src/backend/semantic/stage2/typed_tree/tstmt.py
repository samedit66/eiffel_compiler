from abc import ABC
from dataclasses import dataclass, field

from .tables import Type
from .texpr import TypedExpr, TypedFeatureCall


class TypedStatement(ABC):
    pass


@dataclass(kw_only=True)
class TypedAssignment(TypedStatement):
    target: TypedExpr
    value: TypedExpr


@dataclass(kw_only=True)
class TypedCreateStmt(TypedStatement):
    create_type: Type
    constructor_call: TypedFeatureCall


@dataclass(kw_only=True)
class TypedElseifBranch(TypedStatement):
    condition: TypedExpr
    body: list[TypedStatement]


@dataclass(kw_only=True)
class TypedIfStmt(TypedStatement):
    condition: TypedExpr
    then_branch: list[TypedStatement]
    else_branch: list[TypedStatement]
    elseif_branches: list[TypedElseifBranch]


@dataclass(kw_only=True)
class TypedLoopStmt(TypedStatement):
    init_stmts: list[TypedStatement]
    until_cond: TypedExpr
    body: list[TypedStatement]
