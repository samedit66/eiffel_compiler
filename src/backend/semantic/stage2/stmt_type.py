from ...tree.stmts.types import *

from .expr_type import type_of_expr

from .errors import *


def check_assignment(assignment: Assignment, type_scope, caller, in_method) -> None:
    target_type = type_of_expr(
        assignment.target,
        type_scope,
        caller,
        in_method,
    )

    value_type = type_of_expr(
        assignment.value,
        type_scope,
        caller,
        in_method,
    )

    if not value_type.conforms_to(target_type):
        raise TypeMismatchError(f"Assignment type mismatch: target is {target_type.name}, but value is {value_type.name}")


def check_routine_call(routine_call: RoutineCall, type_scope, caller, in_method) -> None:
    type_of_expr(routine_call.feature_call, type_scope, caller, in_method)
