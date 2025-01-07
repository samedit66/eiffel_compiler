from __future__ import annotations
from tree.base import *
from tree.type_decl.types import *


def make_type_decl(type_decl_dict: dict) -> TypeDecl:
    match type_decl_dict["type"]:
        case "type_spec":
            return make_simple_type_decl(type_decl_dict)
        case "type_spec_like":
            return make_like_type_decl(type_decl_dict)
        case "generic_type_spec":
            return make_generic_type_decl(type_decl_dict)
        case unkwnown_type_decl:
            raise UnknownNodeTypeError(f"Unknown type declaration: {unkwnown_type_decl}")


def make_simple_type_decl(simple_decl_dict: dict) -> TypeDecl:
    location = Location.from_dict(simple_decl_dict["location"])
    match simple_decl_dict["type_name"]:
        case "INTEGER":
            return IntegerType(location)
        case "REAL":
            return RealType(location)
        case "BOOLEAN":
            return BooleanType(location)
        case "STRING":
            return StringType(location)
        case "CHARACTER":
            return CharacterType(location)
        case "Void":
            return VoidType(location)
        case type_name:
            return ClassType(location, type_name, [])


def make_like_type_decl(like_decl_dict: dict) -> TypeDecl:
    location = Location.from_dict(like_decl_dict["location"])
    like_what_value = like_decl_dict["like_what"]
    match like_what_value["type"]:
        case "current_const":
            return LikeCurrentType(location)
        case "ident_lit":
            return LikeOtherFieldType(location, like_what_value["value"])
        case unknown_value:
            raise UnknownNodeTypeError(f"Unknown value type of like spec: {unknown_value}")


def make_generic_type_decl(generic_decl_dict: dict) -> TypeDecl:
    location = Location.from_dict(generic_decl_dict["location"])
    type_list = generic_decl_dict["type_list"]
    match generic_decl_dict["type_name"]:
        case "ARRAY":
            elements_type = TypeDecl.from_dict(type_list[0])
            return ArrayType(location, elements_type)
        case "TUPLE":
            elements_type_list = [TypeDecl.from_dict(element_type) for element_type in type_list]
            return TupleType(location, elements_type_list)
        case type_name: # Определяемый пользователем тип
            type_list = [TypeDecl.from_dict(element_type) for element_type in type_list]
            return ClassType(location, type_name, type_list)
