from __future__ import annotations

from tree.base import *
from tree.expr.types import *


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
    ...


def make_precursor_call(precursor_call_dict: dict) -> PrecursorCall:
    ...


def make_bracket_access(bracket_access_dict: dict) -> BracketAccess:
    ...


def make_if_expr(if_expr_dict: dict) -> IfExpr:
    ...


def make_create_expr(create_expr_dict: dict) -> CreateExpr:
    ...


def make_bin_op(bin_op_dict: dict) -> BinaryOp:
    ...


def make_unary_op(unary_op_dict: dict) -> UnaryOp:
    ...
