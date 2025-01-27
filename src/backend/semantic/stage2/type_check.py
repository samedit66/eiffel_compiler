from ...tree.expr.types import *

from .types import *
from .expr_type import type_of_expr, type_of_constant


def check_constant_type(constant: TypedConstant, type_scope: TypeScope) -> None:
    const_val = constant.value
    if not isinstance(const_val, ConstantValue):
        raise ValueError(f"Couldn't infer type of constant {const_val}")
    
    value_type = type_of_constant(const_val, type_scope)


def check_feature_type(feature: TypedFeature, defined_in: TypedClass) -> None:
    ...


def check_type_of_class(tc: TypedClass) -> None:
    for feature in tc.iterfeatures():
        # Никогда не сработает, просто для того чтобы тип feature далее
        # считался как TypedFeature
        assert isinstance(feature, TypedFeature), "Should never occur"

        