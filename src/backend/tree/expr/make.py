from __future__ import annotations

from ..base import *
from ..expr.types import *


def make_expr(expr_dict: dict) -> Expr:
    location = Location.from_dict(expr_dict["location"])
    match expr_dict["type"]:
        case "int_const":
            return IntegerConst(
                location=location,
                value=expr_dict["value"],
                )
        case "real_const":
            return RealConst(
                location=location,
                value=expr_dict["value"],
                )
        case "char_const":
            return CharacterConst(
                location=location,
                value=expr_dict["value"]
            )
        case "string_const":
            unescaped = (expr_dict["value"]
                .encode("raw_unicode_escape")
                .decode("unicode_escape")
                )
            return StringConst(
                location=location,
                value=unescaped,
            )
        case "boolean_const":
            return BoolConst(
                location=location,
                value=expr_dict["value"],
            )
        case "result_const":
            return ResultConst(location=location)
        case "current_const":
            return CurrentConst(location=location)
        case "void_const":
            return VoidConst(location=location)
        case "manifest_tuple":
            return make_manifest_tuple(expr_dict)
        case "manifest_array":
            return make_manifest_array(expr_dict)
        case "feature_call":
            return make_feature_call(expr_dict)
        case "precursor_call":
            return make_precursor_call(expr_dict)
        case "bracket_access":
            return make_bracket_access(expr_dict)
        case "if_expr":
            return make_if_expr(expr_dict)
        case "create_expr":
            return make_create_expr(expr_dict)
        case expr_type:
            try:
                return make_bin_op(expr_dict)
            except UnknownNodeTypeError: pass

            try:
                return make_unary_op(expr_dict)
            except UnknownNodeTypeError: pass

            raise UnknownNodeTypeError(f"Unknown expression type: {expr_type}")


def make_manifest_tuple(manifest_tuple_dict: dict) -> ManifestTuple:
    return ManifestTuple(
        location=Location.from_dict(manifest_tuple_dict["location"]),
        values=[make_expr(value) for value in manifest_tuple_dict["content"]],
    )


def make_manifest_array(manifest_array_dict: dict) -> ManifestArray:
    return ManifestArray(
        location=Location.from_dict(manifest_array_dict["location"]),
        values=[make_expr(value) for value in manifest_array_dict["content"]],
    )


def make_feature_call(feature_call_dict: dict) -> FeatureCall:
    return FeatureCall(
        location=Location.from_dict(feature_call_dict["location"]),
        feature_name=feature_call_dict["feature"]["name"],
        arguments=[make_expr(arg) for arg in feature_call_dict["feature"]["args_list"]],
        owner=None if is_empty_node(feature_call_dict["owner"]) else make_expr(feature_call_dict["owner"]),
    )


def make_precursor_call(precursor_call_dict: dict) -> PrecursorCall:
    return PrecursorCall(
        location=Location.from_dict(precursor_call_dict["location"]),
        arguments=[make_expr(arg) for arg in precursor_call_dict["args_list"]],
        # TODO: добавить задание типа родителя
    )


def make_bracket_access(bracket_access_dict: dict) -> BracketAccess:
    indices = []
    source = bracket_access_dict

    while source["type"] == "bracket_access":
        indices.append(make_expr(source["index"]))
        source = source["source"]

    return BracketAccess(
        location=Location.from_dict(bracket_access_dict["location"]),
        indexed_expr=make_expr(source),
        indices=indices,
    )


def make_if_expr(if_expr_dict: dict) -> IfExpr:
    return IfExpr(
        location=Location.from_dict(if_expr_dict["location"]),
        condition=make_expr(if_expr_dict["cond"]),
        then_expr=make_expr(if_expr_dict["then_expr"]),
        else_expr=make_expr(if_expr_dict["else_expr"]),
        elseif_exprs=[
            ElseifExprBranch(
                location=Location.from_dict(elseif_expr_dict["location"]),
                condition=make_expr(elseif_expr_dict["cond"]),
                expr=make_expr(elseif_expr_dict["expr"]),
            )
            for elseif_expr_dict in if_expr_dict["elseif_exprs"]
        ]
    )


def make_create_expr(create_expr_dict: dict) -> CreateExpr:
    return CreateExpr(
        location=Location.from_dict(create_expr_dict["location"]),
        type_name=create_expr_dict["type_name"],
        constructor_call=(
            None if is_empty_node(create_expr_dict["constructor_call"])
            else make_feature_call(create_expr_dict["constructor_call"])
            ),
    )


def make_bin_op(bin_op_dict: dict) -> BinaryOp:
    bin_type_mapping = {
        "add_op": AddOp,
        "sub_op": SubOp,
        "mul_op": MulOp,
        "div_op": DivOp,
        "int_div_op": IntDivOp,
        "mod_op": ModOp,
        "pow_op": PowOp,
        "and_op": AndOp,
        "or_op": OrOp,
        "and_then_op": AndThenOp,
        "or_else_op": OrElseOp,
        "implies_op": ImpliesOp,
        "xor_op": XorOp,
        "lt_op": LtOp,
        "gt_op": GtOp,
        "le_op": LeOp,
        "ge_op": GeOp,
        "eq_op": EqOp,
        "neq_op": NeqOp,
    }

    node_type = bin_op_dict["type"]
    op_class = bin_type_mapping.get(node_type)
    if op_class is None:
        raise UnknownNodeTypeError(f"Unknown binary expression type: {node_type}")

    if hasattr(op_class, "to_feature_call"):
        return op_class.to_feature_call()

    return op_class(
        location=Location.from_dict(bin_op_dict["location"]),
        left=make_expr(bin_op_dict["left"]),
        right=make_expr(bin_op_dict["right"]),
    )


def make_unary_op(unary_op_dict: dict) -> UnaryOp:
    unary_op_mapping = {
        "unary_minus_op": MinusOp,
        "unary_plus_op": PlusOp,
        "not_op": NotOp,
    }

    node_type = unary_op_dict["type"]
    op_class = unary_op_mapping.get(node_type)
    if op_class is None:
        raise UnknownNodeTypeError(f"Unknown unary expression type: {node_type}")
    
    if hasattr(op_class, "to_feature_call"):
        return op_class.to_feature_call()

    return op_class(
        location=Location.from_dict(unary_op_dict["location"]),
        argument=make_expr(unary_op_dict["arg"]),
    )
