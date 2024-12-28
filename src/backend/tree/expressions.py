from __future__ import annotations
from abc import ABC
from dataclasses import (
    dataclass,
    field,
)


class Expression(ABC):
    
    @classmethod
    def from_dict(cls, expr_dict: dict) -> Expression:
        return None
    

type ExpressionSequence = list[Expression]


class ConstantValue(Expression, ABC):
    pass


@dataclass
class IntegerConst(ConstantValue):
    value: int


@dataclass
class RealConst(ConstantValue):
    value: float


@dataclass
class CharacterConst(ConstantValue):
    value: str


@dataclass
class StringConst(ConstantValue):
    value: str


class ResultConst(ConstantValue):
    pass


class CurrentConst(ConstantValue):
    pass


class TrueConst(ConstantValue):
    pass


class FalseConst(ConstantValue):
    pass


class VoidConst(ConstantValue):
    pass


@dataclass
class TupleConst(ConstantValue):
    values: ExpressionSequence


@dataclass
class ArrayConst(ConstantValue):
    values: ExpressionSequence


@dataclass
class FeatureCall(Expression):
    feature_name: str
    arguments: ExpressionSequence = field(default_factory=list)
    owner: Expression | None = None


@dataclass
class PrecursorCall(Expression):
    arguments: ExpressionSequence = field(default_factory=list)


@dataclass
class CreateExpr(Expression):
    type_name: str
    constructor_call: FeatureCall | None = None


@dataclass
class ElseifBranch(Expression):
    condition: Expression
    then_expr: Expression


@dataclass
class IfExpr(Expression):
    condition: Expression
    then_expr: Expression
    else_expr: Expression
    elseif_exprs: list[ElseifBranch] = field(default_factory=list)


@dataclass
class BracketAccess(Expression):
    indexed_expr: Expression
    indices: ExpressionSequence


@dataclass
class BinaryOp(ABC):
    left: Expression
    right: Expression


@dataclass
class UnaryOp(ABC):
    argument: Expression


class AddOp(BinaryOp):
    pass


class SubOp(BinaryOp):
    pass


class MulOp(BinaryOp):
    pass


class DivOp(BinaryOp):
    pass


class MinusOp(UnaryOp):
    pass


class PlusOp(UnaryOp):
    pass


class IntDiv(BinaryOp):
    pass


class ModOp(BinaryOp):
    pass


class PowOp(BinaryOp):
    pass


class AndOp(BinaryOp):
    pass


class OrOp(BinaryOp):
    pass


class NotOp(UnaryOp):
    pass


class AndThenOp(BinaryOp):
    pass


class OrElseOp(BinaryOp):
    pass


class XorOp(BinaryOp):
    pass


class LtOp(BinaryOp):
    pass


class GtOp(BinaryOp):
    pass


class EqOp(BinaryOp):
    pass


class NeqOp(BinaryOp):
    pass


class LeOp(BinaryOp):
    pass


class GeOp(BinaryOp):
    pass


class ImpliesOp(BinaryOp):
    pass
