from ....tree.expr.types import *

from .tables import TypeHierarchy
from .texpr import *


def make_typed_expr(expr: Expr, type_heirarchy: TypeHierarchy) -> TypedExpr:
    ...


def make_typed_literal(literal: ConstantValue) -> TypedExpr:
    match literal:
        case IntegerConst(value=value):
            return TypedInteger(
                type_of=Type("INTEGER"),
                value=value,
            )
        case RealConst(value=value):
            return TypedReal(
                type_of=Type("REAL"),
                value=value,
            )
        case CharacterConst(value=value):
            return TypedCharacter(
                type_of=Type("CHARACTER"),
                value=value,
            )
        case StringConst(value=value):
            return TypedString(
                type_of=Type("STRING"),
                value=value,
            )
        case BoolConst(value=value):
            return TypedBool(
                type_of=Type("BOOL"),
                value=value,
            )
        case VoidConst():
            return TypedVoid(type_of=Type("Void"))
        

def make_typed_feature_call(feature_call: FeatureCall) -> TypedFeatureCall:
    ...
