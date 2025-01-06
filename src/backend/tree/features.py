from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from tree.base import *
from tree.type_decl import TypeDecl
from tree.statements import StatementList, Assignment
from tree.expressions import Expression, ResultConst, TrueConst


def separate_declarations(decl_node_dict: dict) -> list:
    """Используется для разделения деклараций полей, методов, констант
    и параметров, объявленных "вместе":
    Необходимо объявления вида
            a, b: INTEGER;
    перевести в
            a: INTEGER; b: INTEGER;
    
    Недостаток данного разделения заключается в том, что частично
    теряется информация о месте объявления - сохраняются только номера строк

    :param decl_node_dict: Узел объявления
    :return: Преобразованный, "разделенный", список узлов, также в виде словарей
    """
    separated = []

    node_type = decl_node_dict["type"]
    location = decl_node_dict["location"]

    name_and_type = decl_node_dict["name_and_type"]

    names = name_and_type["names"]
    for name in names:
        name_and_type_ = {
            "field_type": name_and_type["field_type"],
            "name": name
        }
        decl_node_dict_ = {
            **decl_node_dict,
            "type": node_type,
            "location": location,
            "name_and_type": name_and_type_
            }
            
        separated.append(decl_node_dict_)

    return separated


@dataclass
class Feature(Node, ABC):
    """Абстракция представления "фичи": поля, метода или константы объекта"""
    name: Identifier

    @staticmethod
    def from_dict(feature_dict: dict) -> Feature:
        feature_type = feature_dict["type"]
        match feature_type:
            case "class_routine":
                return Method.from_dict(feature_dict)
            case "class_field":
                return Field.from_dict(feature_dict)
            case "class_constant":
                return Constant.from_dict(feature_dict)
            case _:
                raise UnknownNodeTypeError(f"Unknown feature type: {feature_type}")


@dataclass(match_args=True)
class Field(Feature):
    value_type: TypeDecl

    @classmethod
    def from_dict(cls, class_field: dict) -> Field:
        location = Location.from_dict(class_field["location"])
        names_list = class_field["name_and_type"]["name"]
        value_type = TypeDecl.from_dict(class_field["name_and_type"]["field_type"])
        return cls(location, names_list, value_type)


@dataclass(match_args=True)
class Constant(Feature):
    value_type: TypeDecl
    constant_value: Expression

    @classmethod
    def from_dict(cls, class_constant: dict) -> Constant:
        location = Location.from_dict(class_constant["location"])
        names_list = class_constant["name_and_type"]["name"]
        value_type = TypeDecl.from_dict(class_constant["name_and_type"]["field_type"])
        constant_value = Expression.from_dict(class_constant["constant_value"])
        return cls(location, names_list, value_type, constant_value)


@dataclass(match_args=True)
class Method(Feature):
    is_deferred: bool
    return_value_type: TypeDecl
    parameters: ParameterList
    do_section: DoSection
    local_section: LocalSection
    require_section: RequireSection
    ensure_section: EnsureSection

    @staticmethod
    def unwrap_then_section(
            then_section: ThenSection,
            do_section: DoSection | None
            ) -> DoSection:
        result_assignment = then_section.to_result_assignment()

        statements = [] if do_section is None else do_section.body.statements
        updated_do_section = DoSection(
            StatementList(
                [*statements, result_assignment]
                )
            )
        return updated_do_section

    @classmethod
    def from_dict(cls, class_routine: dict) -> Method:
        location = Location.from_dict(class_routine["location"])

        name = class_routine["name_and_type"]["name"]
        return_value_type = TypeDecl.from_dict(class_routine["name_and_type"]["field_type"])
        parameters = ParameterList.from_list(class_routine["params"])

        routine_dict = class_routine["body"]

        is_deferred = routine_dict["is_deferred"]

        local_section = LocalSection.from_list(routine_dict["local"])
        require_section = RequireSection.from_list(routine_dict["require"])
        ensure_section = EnsureSection.from_list(routine_dict["ensure"])

        # Убираем синтаксический сахар: then-секция превращается в
        # присвоение к переменной Result выражения, записанного в then-секции
        do_section = DoSection.from_list(routine_dict["do"])
        then_section_node = routine_dict["then"]
        if not is_empty_node(then_section_node):
            then_section = ThenSection.from_dict(routine_dict["then"])
            do_section = Method.unwrap_then_section(then_section, do_section)

        return cls(
            location=location,
            name=name,
            is_deferred=is_deferred,
            return_value_type=return_value_type,
            parameters=parameters,
            do_section=do_section,
            local_section=local_section,
            require_section=require_section,
            ensure_section=ensure_section,
            )


@dataclass(match_args=True)
class Parameter(Node):
    name: Identifier
    parameter_type: TypeDecl

    @classmethod
    def from_dict(cls, parameter_dict: dict) -> Parameter:
        location = Location.from_dict(parameter_dict["location"])
        
        name_and_type = parameter_dict["name_and_type"]

        name = name_and_type["name"]

        parameter_type_node = name_and_type["field_type"]
        parameter_type = TypeDecl.from_dict(parameter_type_node)

        return cls(location, name, parameter_type)


@dataclass(match_args=True)
class ParameterList:
    parameters: list[Parameter]

    @classmethod
    def from_list(cls, parameters: list) -> ParameterList:
        separated = [p_ for p in parameters for p_ in separate_declarations(p)]
        return cls([Parameter.from_dict(parameter_dict) for parameter_dict in separated])


type VariableDecl = Field


@dataclass(match_args=True)
class LocalSection:
    variables: list[VariableDecl]

    @classmethod
    def from_list(cls, var_decls: list) -> LocalSection:
        separated = [v_ for v in var_decls for v_ in separate_declarations(v)]
        variables = [Field.from_dict(var_decl) for var_decl in separated]
        return cls(variables)


@dataclass(match_args=True)
class Condition(Node):
    condition_expr: Expression
    tag: str | None = None

    @classmethod
    def always_true(cls) -> Condition:
        return cls(location=None, condition_expr=TrueConst(None))

    @classmethod
    def from_dict(cls, cond_dict: dict) -> Condition:
        location = Location.from_dict(cond_dict["location"])
        condition_expr = Expression.from_dict(cond_dict["cond"])
        tag = cond_dict.get("tag")
        return cls(location, condition_expr, tag)


@dataclass(match_args=True)
class RequireSection:
    conditions: list[Condition]

    @classmethod
    def from_list(cls, cond_list: list) -> RequireSection:
        # Убираем синтаксический сахар: пустой список предусловий эквивалентен
        # одному всегда истинному предусловию
        conditions = [Condition.from_dict(cond) for cond in cond_list] or [Condition.always_true()]
        return cls(conditions)


@dataclass(match_args=True)
class EnsureSection:
    conditions: list[Condition]

    @classmethod
    def from_list(cls, cond_list: list) -> EnsureSection:
        # Убираем синтаксический сахар: пустой список постусловий эквивалентен
        # одному всегда истинному постусловию
        conditions = [Condition.from_dict(cond) for cond in cond_list] or [Condition.always_true()]
        return cls(conditions)


@dataclass(match_args=True)
class DoSection:
    body: StatementList

    @classmethod
    def from_list(cls, do_list: list) -> DoSection:
        return cls(StatementList.from_list(do_list))


@dataclass(match_args=True)
class ThenSection:
    result_expr: Expression

    def to_result_assignment(self) -> Assignment:
        location = self.result_expr.location
        target = ResultConst(location)
        value = self.result_expr
        return Assignment(location, target, value)

    @classmethod
    def from_dict(cls, expr_dict: dict) -> ThenSection:
        return cls(Expression.from_dict(expr_dict))


@dataclass(match_args=True)
class FeatureList:
    clients: IdentifierList
    features: list[Feature]

    @classmethod
    def from_list(cls, features_dict: dict) -> FeatureList:
        # Убираем синтаксический сахар: если список клиентов пустой,
        # это означает, что метод доступен для вызова кому-угодно
        clients = features_dict["clients"] or ["ANY"]

        features = [
            Feature.from_dict(f_)
            for f in features_dict["feature_list"]
            for f_ in separate_declarations(f)
        ]

        return cls(clients, features)
