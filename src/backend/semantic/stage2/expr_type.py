from ...tree.expr.types import *
from ...tree.stmts.types import *

from .types import (
    Binding,
    TypedFeature,
    TypedMethod,
    TypeScope,
    TypedClass,
    TypedLocal,
    TypedConstant,
    TypedField,
    Scope,
)

from .errors import *


def type_of_expr(
        expr: Expr | str,
        type_scope: TypeScope,
        caller: TypedClass,
        in_method: TypedMethod | None = None,
) -> TypedClass:
    if isinstance(expr, ConstantValue):
        return type_of_constant(expr, type_scope)

    assert in_method is not None, "Should never occur"

    context = in_method.local_scope
    if isinstance(expr, str):
        ...

    match expr:
        case ResultConst():
            result_type = context.find("Result")
            if result_type is None:
                raise ValueError("Couldn't get type of Result - seems like you're inside a procedure")
            
            return result_type
        case CurrentConst():
            result_type = context.find("Current")
            if result_type is None:
                raise ValueError("Couldn't get type of Current")
            
            return result_type
        case FeatureCall():
            return type_of_feature_call(expr, in_method, caller, type_scope)
        case PrecursorCall():
            # Ужасный недостаток данной функции состоит в том, что
            # она является мутирующей - к сожалению, это единственный способ
            # как можно протащить имя переопределенной функции без сильных костылей
            if expr.feature_name is not None:
                expr.feature_name = in_method.name
            # Без понятия может ли такое случится, но если случилось, то это ошибка
            assert expr.feature_name == in_method.name
            return in_method.type_of
        case CreateExpr():
            create_type = type_scope.find(expr.type_name)
            if create_type is None:
                raise ValueError(f"Type {expr.type_name} is not in the global type scope")

            return create_type
        case BracketAccess():
            raise NotImplementedError
        case BinaryOp():
            # Для всех других BinaryOp определен эквивалентный FeatureCall
            return type_of_bin_logical_op(expr, in_method, caller, type_scope)
        case UnaryOp():
            # Для всех других UnaryOp определен эквивалентный FeatureCall
            return type_of_not_op(expr, in_method, caller, type_scope)
        case IfExpr():
            return type_of_if_expr(expr, in_method, caller, type_scope)


def type_of_constant(const: ConstantValue, type_scope: TypeScope) -> TypedClass:
    match const:
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
            return type_scope.find("Void")

    raise ValueError(f"Couldn't infer type of constant {const}")


def type_of_bin_logical_op(bin_op: BinaryOp, type_scope: TypeScope, caller: TypedClass, in_method: TypedMethod) -> TypedClass:
    left_type = type_of_expr(bin_op.left, type_scope, caller, in_method)
    right_type = type_of_expr(bin_op.right, type_scope, caller, in_method)

    mapping = {
        AndOp: "and",
        OrOp: "or",
        AndThenOp: "and then",
        OrElseOp: "or else",
        XorOp: "xor",
        ImpliesOp: "implies",
    }

    operation_name = mapping.get(type(bin_op))
    assert operation_name is not None

    if left_type.name != "BOOLEAN" or right_type.name != "BOOLEAN":
        raise TypeMismatchError(
            f"Operation '{operation_name}' requires BOOLEAN types, "
            f"but got {left_type.name} and {right_type.name}."
        )

    return type_scope.find("BOOLEAN")


def type_of_not_op(expr: UnaryOp, type_scope: TypeScope, caller: TypedClass, in_method: TypedMethod) -> TypedClass:
    operand_type = type_of_expr(expr.operand, type_scope, caller, in_method)

    if operand_type.name != "BOOLEAN":
        raise TypeMismatchError(f"Unary NOT operation requires BOOLEAN type, got {operand_type.name}")

    return type_scope.find("BOOLEAN")


def type_of_if_expr(if_expr: IfExpr, type_scope: TypeScope, caller: TypedClass, in_method: TypedMethod) -> TypedClass:
    # Проверяем, что условие основного if имеет тип BOOLEAN
    condition_type = type_of_expr(if_expr.condition, type_scope, caller, in_method)
    if condition_type.name != "BOOLEAN":
        raise TypeMismatchError(f"If condition must be of type BOOLEAN, got {condition_type.name}")

    # Определяем тип then_expr и else_expr
    then_type = type_of_expr(if_expr.then_expr, type_scope, caller, in_method)
    else_type = type_of_expr(if_expr.else_expr, type_scope, caller, in_method)

    if then_type.name != else_type.name:
        raise TypeMismatchError(
            f"The types of 'then' and 'else' branches must match. Got {then_type.name} and {else_type.name}"
        )

    # Проверяем elseif ветки
    for branch in if_expr.elseif_exprs:
        branch_condition_type = type_of_expr(branch.condition, type_scope, caller, in_method)
        if branch_condition_type.name != "BOOLEAN":
            raise TypeMismatchError(
                f"Elseif condition must be of type BOOLEAN, got {branch_condition_type.name}"
            )

        branch_expr_type = type_of_expr(branch.expr, type_scope, caller, in_method)
        if branch_expr_type.name != then_type.name:
            raise TypeMismatchError(
                f"The type of 'elseif' branch must match the type of 'then' and 'else' branches. "
                f"Expected {then_type.name}, got {branch_expr_type.name}"
            )

    return then_type


def check_feature_signatures(
        feature_call: FeatureCall,
        binding: Binding,
        type_scope: TypeScope,
        caller: TypedClass,
        in_method: TypedMethod,
) -> None:
    # Получаем типы всех аргументов переданных непосредственно
    actuals = [
        type_of_expr(arg, type_scope, caller, in_method)
        for arg in feature_call.arguments
    ]

    if (isinstance(binding, (TypedLocal, TypedField, TypedConstant)) and
            len(actuals) > 0):
        raise ValueError("Wrong number of arguments given")
    
    if isinstance(binding, TypedMethod):
        parameters = binding.parameters

        if len(actuals) != len(parameters):
            raise ValueError("Wrong number of arguments given")
        
        for actual_arg, parameter in zip(actuals, (p.type_of for p in parameters)):
            if not actual_arg.conforms_to(parameter):
                raise ValueError("Wrong type of argument")

    assert False


def type_of_feature_call(
        feature_call: FeatureCall,
        in_method: TypedMethod,
        caller: TypedClass,
        type_scope: TypeScope,
) -> TypedClass:
    context = in_method.local_scope

    # 1. Определить тип объекта, у котрого вызывается фича
    if feature_call.owner is not None:
        # Тут будет выброс исключения, если владелец фичи не существует
        owner_type = type_of_expr(
            expr=feature_call.owner,
            type_scope=type_scope,
            caller=caller,
            in_method=in_method,
            )
    else:
        owner_type = None

    # 2. Если фича вызывается локально...
    if owner_type is None:
        binding = context.find(feature_call.name)

        # Была попытку вызвать несуществующую фичу
        if binding is None:
            raise ValueError(f"Feature {feature_call.name} doesn't exist")

        check_feature_signatures(feature_call, binding)
    # 3. Иначе если вызываемая фича принадлежит другому объекту...
    else:
        # Определить, может ли вообще caller вызвать данную фичу.
        # Минус в том, что сюда попадает и случай когда такой фичи у owner_type нет
        if not owner_type.responds_to(feature_call.name, caller):
            raise ValueError(f"Class {caller.name} not allowed to call feature {feature_call.name} of {caller.name}")
        
        binding = owner_type.features_scope.find(feature_call.name)
        assert binding is not None, "Should never occur"

        check_feature_signatures(feature_call, binding)
    
    return binding.type_of
