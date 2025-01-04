from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field

from tree.base import Location, Node, UnknownNodeTypeError


class TypeDecl(Node, ABC):
    
    @staticmethod
    def from_dict(type_decl_dict: dict) -> TypeDecl:
        location = Location.from_dict(type_decl_dict["location"])
        node_type = type_decl_dict["type"]

        if node_type == "type_spec":
            type_name = type_decl_dict["type_name"]
            match type_name:
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
                case _:
                    return ClassType(location, type_name, [])
        elif node_type == "type_spec_like":
            like_what_value = type_decl_dict["like_what"]

            value_type = like_what_value["type"]
            if value_type == "current_const":
                return LikeCurrentType(location)
            elif value_type == "ident_lit":
                ident = like_what_value["value"]
                return LikeOtherFieldType(location, ident)
            else:
                raise UnknownNodeTypeError(f"Unknown value type of like spec: {node_type}")
        elif node_type == "generic_type_spec":
            type_list = type_decl_dict["type_list"]
            type_name = type_decl_dict["type_name"]

            if type_name == "ARRAY":
                elements_type = TypeDecl.from_dict(type_list[0])
                return ArrayType(location, elements_type)
            elif type_name == "TUPLE":
                type_list = [TypeDecl.from_dict(element_type) for element_type in type_list]
                return TupleType(location, type_list)
            else: # Определяемый пользователем тип
                type_list = [TypeDecl.from_dict(element_type) for element_type in type_list]
                return ClassType(location, type_name, type_list)
        else:
            raise UnknownNodeTypeError(f"Unknown type declaration: {node_type}")



class IntegerType(TypeDecl):
    pass


class RealType(TypeDecl):
    pass


class BooleanType(TypeDecl):
    pass


class StringType(TypeDecl):
    pass


class CharacterType(TypeDecl):
    pass


class VoidType(TypeDecl):
    pass


@dataclass(match_args=True)
class ArrayType(TypeDecl):
    elements_type: TypeDecl


@dataclass(match_args=True)
class TupleType(TypeDecl):
    elements_type_list: list[TypeDecl] = field(default_factory=list)


@dataclass(match_args=True)
class ClassType(TypeDecl):
    type_name: str
    generics: list[TypeDecl] = field(default_factory=list)


@dataclass
class GenericType:
    template_type_name: str
    required_ancestor: TypeDecl | None = None


@dataclass
class LikeCurrentType(TypeDecl):
    pass


@dataclass
class LikeOtherFieldType(TypeDecl):
    other_field_name: str
