from serpent.tree.expr import *

from serpent.semantic_checker.typed_tree import TypedExpr, Type


def type_of_constant(constant_expr: ConstantValue) -> TypedExpr:
    match constant_expr:
        case IntegerConst():
            return TypedExpr(Type("INTEGER"), constant_expr)
        case RealConst():
            return TypedExpr(Type("REAL"), constant_expr)
        case CharacterConst():
            return TypedExpr(Type("CHARACTER"), constant_expr)
        case StringConst():
            return TypedExpr(Type("STRING"), constant_expr)
        case BoolConst():
            return TypedExpr(Type("BOOLEAN"), constant_expr)
        case VoidConst():
            return TypedExpr(Type("NONE"), constant_expr)
        case _:
            raise ValueError("This should never happen")
