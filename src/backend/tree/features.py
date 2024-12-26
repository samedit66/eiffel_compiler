from __future__ import annotations
from abc import ABC
from dataclasses import (
    dataclass,
    field,
)

from base import IdentifierList
from type_decl import ConcreteType
from constants import ConstantValue
from statements import StatementList


class Feature(ABC):
    pass


@dataclass
class Field(Feature):
    name: IdentifierList
    value_type: ConcreteType


@dataclass
class Constant(Feature):
    name: IdentifierList
    constant_type: ConcreteType
    constant_value: ConstantValue


type Parameter = Field

@dataclass
class ParameterList:
    parameters: list[Parameter] = field(default_factory=list)


@dataclass
class Method(Feature):
    name: IdentifierList
    return_type: ConcreteType
    parameters: ParameterList


@dataclass
class FeatureList:
    clients: IdentifierList = field(default_factory=list)
    features: list[Feature] = field(default_factory=list)
