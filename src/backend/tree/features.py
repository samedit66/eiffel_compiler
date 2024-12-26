from __future__ import annotations
from abc import ABC
from dataclasses import (
    dataclass,
    field,
)

from base import IdentifierList
from type_decl import ConcreteType
from statements import StatementList
from expressions import (
    Expression,
    ConstantValue,
)


class Feature(ABC):
    pass


@dataclass
class Field(Feature):
    names_list: IdentifierList
    value_type: ConcreteType

    @classmethod
    def from_dict(cls, class_field: dict) -> Field:
        names_list = class_field["name_and_type"]["names"]
        value_type = ConcreteType.from_dict(class_field["name_and_type"]["field_type"])
        return cls(names_list, value_type)


@dataclass
class Constant(Feature):
    name: IdentifierList
    constant_type: ConcreteType
    constant_value: ConstantValue

    @classmethod
    def from_dict(cls, class_field: dict) -> Constant:
        names_list = class_field["name_and_type"]["names"]
        value_type = ConcreteType.from_dict(class_field["name_and_type"]["field_type"])
        return cls(names_list, value_type)


type Parameter = Field

@dataclass
class ParameterList:
    parameters: list[Parameter] = field(default_factory=list)

    @classmethod
    def from_list(cls, params: list) -> ParameterList:
        parameters = [Field.from_dict(param) for param in params]
        return cls(parameters)


type VariableDecl = Field

@dataclass
class LocalSection:
    variables: list[VariableDecl] = field(default_factory=list)

    @classmethod
    def from_list(cls, var_decls: list) -> LocalSection:
        variables = [Field.from_dict(var_decl) for var_decl in var_decls]
        return cls(variables)


@dataclass
class Condition:
    condition_expr: Expression
    tag: str | None = None

    @classmethod
    def from_dict(cls, cond_dict: dict) -> Condition:
        condition_expr = Expression.from_dict(cond_dict["cond"])
        tag = cond_dict.get("tag")
        return cls(condition_expr, tag)


@dataclass
class RequireSection:
    conditions: list[Condition] = field(default_factory=list)

    @classmethod
    def from_list(cls, cond_list: list) -> RequireSection:
        conditions = [Condition.from_dict(cond) for cond in cond_list]
        return cls(conditions)


@dataclass
class DoSection:
    body: StatementList

    @classmethod
    def from_list(cls, do_dict: dict) -> DoSection:
        return StatementList.from_list(do_dict["do"])


@dataclass
class ThenSection:
    result_expr: Expression

    @classmethod
    def from_dict(cls, expr_dict: dict) -> ThenSection:
        return cls(Expression.from_dict(expr_dict))


@dataclass
class EnsureSection:
    conditions: list[Condition] = field(default_factory=list)

    @classmethod
    def from_list(cls, cond_list: list) -> EnsureSection:
        conditions = [Condition.from_dict(cond) for cond in cond_list]
        return cls(conditions)


@dataclass
class Method(Feature):
    name: IdentifierList
    return_type: ConcreteType
    parameters: ParameterList
    local_section: LocalSection
    require_section: RequireSection
    do_section: DoSection
    then_section: ThenSection
    ensure_section: EnsureSection

    @classmethod
    def from_dict(cls, class_routine: dict) -> Method:
        names_list = class_routine["name_and_type"]["names"]
        return_type = ConcreteType.from_dict(class_routine["name_and_type"]["field_type"])
        parameters = ParameterList.from_list(class_routine["params"])


@dataclass
class FeatureList:
    clients: IdentifierList = field(default_factory=list)
    features: list[Feature] = field(default_factory=list)
