from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field


class Type(ABC):
    pass


class ConcreteType(Type, ABC):
    
    @classmethod
    def from_dict(cls, type_dict: dict) -> ConcreteType:
        node_type = type_dict["type"]
        type_name = type_dict["type_name"]

        if node_type == "type_spec":
            match type_dict["type_name"]:
                case "INTEGER":
                    return IntegerType()
                case "REAL":
                    return RealType()
                case "BOOLEAN":
                    return BooleanType()
                case "STRING":
                    return StringType()
                case "CHARACTER":
                    return CharacterType()
                case "Void":
                    return VoidType()
                case _:
                    return UserDefinedClassType(type_name)
        else: # type_dict["type"] == "generic_type_spec"
            type_list = type_dict["type_list"]

            if type_name == "ARRAY":
                elements_type = ConcreteType.from_dict(type_list[0])
                return ArrayType(elements_type)
            elif type_name == "TUPLE":
                type_list = [ConcreteType.from_dict(element_type) for element_type in type_list]
                return TupleType(type_list)
            else: # Определяемый пользователем тип
                type_list = [ConcreteType.from_dict(element_type) for element_type in type_list]
                return UserDefinedClassType(type_name, type_list)


@dataclass
class GenericType(Type):
    name: str
    required_ancestor: ConcreteType | None = None


class IntegerType(ConcreteType):
    pass


class RealType(ConcreteType):
    pass


class BooleanType(ConcreteType):
    pass


class StringType(ConcreteType):
    pass


class CharacterType(ConcreteType):
    pass


class VoidType(ConcreteType):
    pass


@dataclass
class ArrayType(ConcreteType):
    elements_type: ConcreteType


@dataclass
class TupleType(ConcreteType):
    type_list: list[ConcreteType]


@dataclass
class UserDefinedClassType(ConcreteType):
    name: str
    type_list: list[ConcreteType] = field(default_factory=list)
