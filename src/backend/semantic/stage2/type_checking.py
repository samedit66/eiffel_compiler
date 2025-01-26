from ...tree.expr import (
    Expr,
    IntegerConst,
    RealConst,
    CharacterConst,
    StringConst,
    BoolConst,
    VoidConst,
)

from .types import (
    TypedFeature,
    TypeScope,
    TypedClass,
)


def expr_type(
        expr: Expr,
        type_scope: TypeScope,
) -> TypedClass:
    match expr:
        case IntegerConst():
            return type_scope.find("INTEGER")
        case RealConst():
            return type_scope.find("REAL")
        case CharacterConst():
            return type_scope.find("CHARACTER")
        case StringConst():
            return type_scope.find("STRING")
        case BoolConst():
            return type_scope.find("BOOLEAN")
        case VoidConst():
            # Эх...
            return type_scope.find("ANY")
    

def check_feature(feature: TypedFeature, type_scope: TypeScope) -> None:
    ...
