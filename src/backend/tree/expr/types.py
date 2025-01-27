from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from ..base import *


class Expr(Node, ABC): ...


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
    feature_name: str | None = None


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


class AddOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="add",
            owner=self.left,
            arguments=[self.right],
        )


class SubOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="sub",
            owner=self.left,
            arguments=[self.right],
        )


class MulOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="mul",
            owner=self.left,
            arguments=[self.right],
        )


class DivOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="div",
            owner=self.left,
            arguments=[self.right],
        )


class MinusOp(UnaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="neg",
            owner=self.left,
            arguments=[],
        )


class PlusOp(UnaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="pos",
            owner=self.left,
            arguments=[],
        )


class IntDivOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="intdiv",
            owner=self.left,
            arguments=[self.right],
        )


class ModOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="mod",
            owner=self.left,
            arguments=[self.right],
        )


class PowOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="pow",
            owner=self.left,
            arguments=[self.right],
        )


class LtOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="lt",
            owner=self.left,
            arguments=[self.right],
        )


class GtOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="gt",
            owner=self.left,
            arguments=[self.right],
        )


class EqOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="eq",
            owner=self.left,
            arguments=[self.right],
        )


class NeqOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="ne",
            owner=self.left,
            arguments=[self.right],
        )


class LeOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="le",
            owner=self.left,
            arguments=[self.right],
        )


class GeOp(BinaryOp):

    def to_feature_call(self) -> FeatureCall:
        return FeatureCall(
            location=self.location,
            feature_name="ge",
            owner=self.left,
            arguments=[self.right],
        )


class AndOp(BinaryOp): pass


class OrOp(BinaryOp): pass


class NotOp(UnaryOp): pass


class AndThenOp(BinaryOp): pass


class OrElseOp(BinaryOp): pass


class XorOp(BinaryOp): pass


class ImpliesOp(BinaryOp): pass
