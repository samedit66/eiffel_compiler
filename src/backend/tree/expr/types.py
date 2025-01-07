from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from tree.base import *


class Expr(Node, ABC): pass


class ConstantValue(Expr, ABC): pass


@dataclass(match_args=True, kw_only=True)
class IntegerConst(ConstantValue):
    value: int


@dataclass(match_args=True, kw_only=True)
class RealConst(ConstantValue):
    value: float


@dataclass(match_args=True, kw_only=True)
class CharacterConst(ConstantValue):
    value: str


@dataclass(match_args=True, kw_only=True)
class StringConst(ConstantValue):
    value: str


@dataclass(match_args=True, kw_only=True)
class BoolConst(ConstantValue):
    value: bool


class VoidConst(ConstantValue): pass


@dataclass(match_args=True, kw_only=True)
class ManifestTuple(Expr):
    values: list[Expr]


@dataclass(match_args=True, kw_only=True)
class ManifestArray(Expr):
    values: list[Expr]


class ResultConst(Expr): pass


class CurrentConst(Expr): pass


@dataclass(match_args=True, kw_only=True)
class FeatureCall(Expr):
    feature_name: str
    arguments: list[Expr]
    owner: Expr | None = None


@dataclass(match_args=True, kw_only=True)
class PrecursorCall(Expr):
    arguments: list[Expr]
    ancestor_name: str | None = None


@dataclass(match_args=True, kw_only=True)
class CreateExpr(Expr):
    type_name: str
    constructor_call: FeatureCall | None = None


@dataclass(match_args=True, kw_only=True)
class ElseifExprBranch(Expr):
    condition: Expr
    expr: Expr


@dataclass(match_args=True, kw_only=True)
class IfExpr(Expr):
    condition: Expr
    then_expr: Expr
    else_expr: Expr
    elseif_exprs: list[ElseifExprBranch]


@dataclass(match_args=True, kw_only=True)
class BracketAccess(Expr):
    indexed_expr: Expr
    indices: list[Expr]


@dataclass(match_args=True, kw_only=True)
class BinaryOp(Expr):
    left: Expr
    right: Expr


@dataclass(match_args=True, kw_only=True)
class UnaryOp(Expr):
    argument: Expr


class AddOp(BinaryOp): pass


class SubOp(BinaryOp): pass


class MulOp(BinaryOp): pass


class DivOp(BinaryOp): pass


class MinusOp(UnaryOp): pass


class PlusOp(UnaryOp): pass


class IntDiv(BinaryOp): pass


class ModOp(BinaryOp): pass


class PowOp(BinaryOp): pass


class AndOp(BinaryOp): pass


class OrOp(BinaryOp): pass


class NotOp(UnaryOp): pass


class AndThenOp(BinaryOp): pass


class OrElseOp(BinaryOp): pass


class XorOp(BinaryOp): pass


class LtOp(BinaryOp): pass


class GtOp(BinaryOp): pass


class EqOp(BinaryOp):  pass


class NeqOp(BinaryOp): pass


class LeOp(BinaryOp): pass


class GeOp(BinaryOp): pass


class ImpliesOp(BinaryOp): pass
