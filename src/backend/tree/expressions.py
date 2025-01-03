from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from tree.base import (
    UnknownNodeTypeError,
    Node,
    Location,
    is_empty_node,
    )


class Expression(Node, ABC):

    @staticmethod
    def from_dict(expr_dict: dict) -> Expression:
        location = Location.from_dict(expr_dict["location"])
        expr_type = expr_dict["type"]
        match expr_type:
            case "int_const":
                return IntegerConst(location, expr_dict["value"])
            case "real_const":
                return RealConst(location, expr_dict["value"])
            case "char_const":
                return CharacterConst(location, expr_dict["value"])
            case "string_const":
                return StringConst.from_dict(expr_dict)
            case "boolean_const":
                return TrueConst(location) if expr_dict["value"] else FalseConst(location)
            case "result_const":
                return ResultConst(location)
            case "current_const":
                return CurrentConst(location)
            case "void_const":
                return VoidConst(location)
            case "manifest_tuple":
                return TupleLiteral.from_dict(expr_dict)
            case "manifest_array":
                return ArrayLiteral.from_dict(expr_dict)
            case "feature_call":
                return FeatureCall.from_dict(expr_dict)
            case "precursor_call":
                return PrecursorCall.from_dict(expr_dict)
            case "bracket_access":
                return BracketAccess.from_dict(expr_dict)
            case "if_expr":
                return IfExpr.from_dict(expr_dict)
            case "create_expr":
                return CreateExpr.from_dict(expr_dict)
            case _:
                try_bin_op = BinaryOp.from_dict(expr_dict)
                if try_bin_op is not None:
                    return try_bin_op
                
                unary_bin_op = UnaryOp.from_dict(expr_dict)
                if unary_bin_op is not None:
                    return unary_bin_op

                raise UnknownNodeTypeError(f"Unknown expression type: {expr_type}")
    

type ExpressionSequence = list[Expression]


class ConstantValue(Expression, ABC):
    pass


@dataclass(match_args=True)
class IntegerConst(ConstantValue):
    value: int


@dataclass(match_args=True)
class RealConst(ConstantValue):
    value: float


@dataclass(match_args=True)
class CharacterConst(ConstantValue):
    value: str


@dataclass(match_args=True)
class StringConst(ConstantValue):
    value: str

    @staticmethod
    def unescape(s: str) -> str:
        return "a\\nb".encode("raw_unicode_escape").decode("unicode_escape")

    @classmethod
    def from_dict(cls, string_dict: dict) -> StringConst:
        location = string_dict["location"]
        value = StringConst.unescape(string_dict["value"])
        return cls(location, value)


class TrueConst(ConstantValue):
    pass


class FalseConst(ConstantValue):
    pass


class VoidConst(ConstantValue):
    pass


@dataclass(match_args=True)
class TupleLiteral(Expression):
    values: ExpressionSequence

    @classmethod
    def from_dict(cls, tuple_dict: dict) -> TupleLiteral:
        location = Location.from_dict(tuple_dict["location"])
        values = [Expression.from_dict(value) for value in tuple_dict["content"]]
        return cls(location, values)


@dataclass(match_args=True)
class ArrayLiteral(Expression):
    values: ExpressionSequence

    @classmethod
    def from_dict(cls, array_dict: dict) -> ArrayLiteral:
        location = Location.from_dict(array_dict["location"])
        values = [Expression.from_dict(value) for value in array_dict["content"]]
        return cls(location, values)


class ResultConst(Expression):
    pass


class CurrentConst(Expression):
    pass


@dataclass(match_args=True)
class FeatureCall(Expression):
    feature_name: str
    arguments: ExpressionSequence
    owner: Expression | None = None

    @classmethod
    def from_dict(cls, feature_call: dict) -> FeatureCall:
        location = Location.from_dict(feature_call["location"])
        owner = None if is_empty_node(feature_call["owner"]) else Expression.from_dict(feature_call["owner"])
        name = feature_call["feature"]["name"]
        arguments = [Expression.from_dict(argument) for argument in feature_call["feature"]["args_list"]]
        return cls(location, name, arguments, owner)


@dataclass(match_args=True)
class PrecursorCall(Expression):
    arguments: ExpressionSequence

    @classmethod
    def from_dict(cls, precursor_call: dict) -> PrecursorCall:
        location = Location.from_dict(precursor_call["location"])
        arguments = [Expression.from_dict(argument) for argument in precursor_call["args_list"]]
        return cls(location, arguments)


@dataclass(match_args=True)
class CreateExpr(Expression):
    type_name: str
    constructor_call: FeatureCall | None = None

    @classmethod
    def from_dict(cls, create_expr_dict: dict) -> CreateExpr:
        location = Location.from_dict(create_expr_dict["location"])
        type_name = create_expr_dict["type_name"]
        constructor_call = (
            None if is_empty_node(create_expr_dict["constructor_call"])
            else FeatureCall.from_dict(create_expr_dict["constructor_call"])
            )
        return cls(location, type_name, constructor_call)


@dataclass(match_args=True)
class ElseifExprBranch(Expression):
    condition: Expression
    expr: Expression

    @classmethod
    def from_dict(cls, elseif_expr_dict: dict) -> ElseifExprBranch:
        location = Location.from_dict(elseif_expr_dict["location"])
        condition = Expression.from_dict(elseif_expr_dict["cond"])
        expr = Expression.from_dict(elseif_expr_dict["expr"])
        return cls(location, condition, expr)


@dataclass(match_args=True)
class IfExpr(Expression):
    condition: Expression
    then_expr: Expression
    else_expr: Expression
    elseif_exprs: list[ElseifExprBranch]

    @classmethod
    def from_dict(cls, if_expr_dict: dict) -> IfExpr:
        location = Location.from_dict(if_expr_dict["location"])
        condition = Expression.from_dict(if_expr_dict["cond"])
        then_expr = Expression.from_dict(if_expr_dict["then_expr"])
        elseif_exprs = [ElseifExprBranch.from_dict(elseif_expr) for elseif_expr in if_expr_dict["elseif_exprs"]]
        else_expr = Expression.from_dict(if_expr_dict["else_expr"])
        return cls(location, condition, then_expr, else_expr, elseif_exprs)


@dataclass(match_args=True)
class BracketAccess(Expression):
    indexed_expr: Expression
    indices: ExpressionSequence

    @classmethod
    def from_dict(cls, bracket_access_dict: dict) -> BracketAccess:
        location = Location.from_dict(bracket_access_dict["location"])

        indices = []

        source = bracket_access_dict
        while source["type"] == "bracket_access":
            index = Expression.from_dict(source["index"])
            indices.append(index)
            source = source["source"]
        
        indices.append(Expression.from_dict(source["index"]))
        source = Expression.from_dict(source)
        return cls(location, source, indices)


@dataclass(match_args=True)
class BinaryOp(Expression):
    left: Expression
    right: Expression

    @staticmethod
    def from_dict(bin_op_dict: dict) -> BinaryOp | None:
        left_node = bin_op_dict.get("left")
        if left_node is None: return None
        
        right_node = bin_op_dict.get("right")
        if right_node is None: return None

        location = Location.from_dict(bin_op_dict["location"])
        node_type = bin_op_dict["type"]
        left = Expression.from_dict(left_node)
        right = Expression.from_dict(right_node)
        match node_type:
            case "add_op":
                return AddOp(location, left, right)
            case "sub_op":
                return SubOp(location, left, right)
            case "mul_op":
                return MulOp(location, left, right)
            case "div_op":
                return DivOp(location, left, right)
            case "int_div_op":
                return IntDiv(location, left, right)
            case "mod_op":
                return ModOp(location, left, right)
            case "pow_op":
                return PowOp(location, left, right)
            case "and_op":
                return AndOp(location, left, right)
            case "or_op":
                return OrOp(location, left, right)
            case "and_then_op":
                return AndThenOp(location, left, right)
            case "or_else_op":
                return OrElseOp(location, left, right)
            case "implies_op":
                return ImpliesOp(location, left, right)
            case "xor_op":
                return XorOp(location, left, right)
            case "lt_op":
                return LtOp(location, left, right)
            case "gt_op":
                return GtOp(location, left, right)
            case "eq_op":
                return EqOp(location, left, right)
            case "neq_op":
                return NeqOp(location, left, right)
            case "le_op":
                return LeOp(location, left, right)
            case "ge_op":
                return GeOp(location, left, right)
            case _:
                raise UnknownNodeTypeError(f"Unknown binary expression type: {node_type}")


@dataclass(match_args=True)
class UnaryOp(Expression):
    argument: Expression

    @staticmethod
    def from_dict(unary_op_dict: dict) -> UnaryOp | None:
        argument_node = unary_op_dict.get("arg")
        if argument_node is None: return None

        argument = Expression.from_dict(argument_node)
        location = Location.from_dict(unary_op_dict["location"])
        node_type = unary_op_dict["type"]
        match node_type:
            case "unary_minus_op":
                return MinusOp(location, argument)
            case "unary_plus_op":
                return PlusOp(location, argument)
            case "not_op":
                return NotOp(location, argument)
            case _:
                raise UnknownNodeTypeError(f"Unknown unary expression type: {node_type}")


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
