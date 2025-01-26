from __future__ import annotations
from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from itertools import groupby

from ...tree.features import (
    Constant,
    Field,
    BaseMethod,
    Method,
    Feature,
    LocalVarDecl,
    Parameter,
)
from ...tree.type_decl import (
    TypeDecl,
    ClassType,
    TupleType,
    LikeCurrent,
    LikeFeature,
    GenericSpec,
)
from ...tree.expr import Expr

from ..stage1 import FlattenClass
from ..stage1.featureset import FeatureSet

from .types import *


def type_decl_of(something) -> TypeDecl:
    if isinstance(something, (Field, Constant, Parameter, LocalVarDecl)):
        type_decl = something.value_type
    elif isinstance(something, BaseMethod):
        type_decl = something.return_type
    else:
        raise ValueError(f"Does {something} really have a type decl?")
    
    return type_decl


def class_type_of(
        type_decl: TypeDecl,
        context: Scope,
        context_class: FlattenClass,
        types: TypeScope,
) -> TypedClass:
    # Этот костыль надо потом убрать...
    if isinstance(type_decl, TupleType):
        raise NotImplementedError("Tuple types are not supported")
    
    if isinstance(type_decl, ClassType):
        type_ = types.find(type_decl.name)

        if type_ is None:
            raise ValueError(f"Class {type_decl.name} not found in global type scope")
    elif isinstance(type_decl, LikeCurrent):
        type_ = types.find(context_class.name)

        if type_ is None:
            raise ValueError(f"Class {type_decl.name} not found in global type scope")
    elif isinstance(type_decl, LikeFeature):
        feature = context.find(type_decl.feature_name)
        if feature is None:
            raise ValueError(f"Unknown feature {type_decl.feature_name} in class {context_class.name}")
        
        type_ = feature.type_of
    else:
        raise ValueError(f"Couldn't find out type of {type_decl}")
    
    # Дикий костыль на то, чтобы запретить типизировать что-либо классом NONE
    if type_.name == "NONE":
        raise ValueError("NONE is not allowed as type anywhere")
    
    return type_


def make_locals(
        var_decls: list[Parameter | LocalVarDecl],
        context: Scope,
        context_class: FlattenClass,
        types: TypeScope, 
) -> list[TypedLocal]:
    local_bindings = []
    duplicates: dict[str, Parameter | LocalVarDecl] = {}

    for name, group in groupby(var_decls, key=lambda x: x.name):
        group = list(group)

        if len(group) > 1:
            duplicates[name] = group
            continue
        
        local = group[0]
        local_type = class_type_of(
            type_decl_of(local),
            context,
            context_class,
            types,
        )
        local_bindings.append(TypedLocal(type_of=local_type, name=local.name))

    if duplicates:
        raise ValueError(duplicates)

    return local_bindings


def make_typed_method(
        method: BaseMethod,
        clients: list[TypedClass],
        context: Scope,
        context_class: FlattenClass,
        types: TypeScope,
) -> TypedMethod:
    method_context = Scope(context)

    # Добавляем в скоуп параметры метода...
    for local in make_locals(method.parameters, context, context_class, types):
        method_context.add(local)

    # ...чтобы на их основании иметь возможность определить,
    # тип возвращаемого значения (полезно в случае like <anchor>)
    return_type = class_type_of(
        type_decl_of(method),
        method_context,
        context_class,
        types,
    )

    # Если это не external-метод, тогда в скоуп метода
    # добавляем и локальные переменные
    if isinstance(method, Method):
        for local in make_locals(method.local_var_decls, context, context_class, types):
            method_context.add(local)

        # Добавляем в скоуп указание на то, какого типа константа Current
        class_type = types.find(context_class.name)
        assert class_type is not None, "Should never occur"
        current = TypedLocal(type_of=class_type, name="Current")
        method_context.add(current)

        # Если метод является функцией, то необходимо добавить
        # неявную переменную Result
        if return_type.name != "Void":
            result = TypedLocal(type_of=return_type, name="Result")
            method_context.add(result)

    return TypedMethod(
        type_of=return_type,
        name=method.name,
        clients=clients,
        method_ref=method,
        local_scope=method_context,
    )


def type_clients(
        feature_clients: list[str],
        types: TypeScope,
) -> list[TypedClass]:
    typed_clients = []
    duplicated = {}
    nonexistent = []

    for class_name, group in groupby(feature_clients):
        group = list(group)

        if len(group) > 1:
            duplicated[class_name] = group
            continue

        client_type = types.find(class_name)
        if client_type is None:
            nonexistent.append(class_name)
            continue

        typed_clients.append(client_type)

    if duplicated:
        raise ValueError(duplicated)
    
    if nonexistent:
        raise ValueError(nonexistent)

    return typed_clients


def make_typed_feature(
        feature: Feature,
        context: Scope,
        context_class: FlattenClass,
        types: TypeScope,
) -> TypedFeature:
    typed_clients = type_clients(feature.clients, types)

    # Дублирование здесь по-хорошему не должно быть,
    # но из-за особенностей добавления в скоупы параметров функций,
    # если вынести make_type будет ошибка...
    if isinstance(feature, Constant):
        return TypedConstant(
            type_of=class_type_of(
                type_decl_of(feature),
                context,
                context_class,
                types,
            ),
            name=feature.name,
            clients=typed_clients,
            value=feature.constant_value,
        )
    elif isinstance(feature, Field):
        return TypedField(
            type_of=class_type_of(
                type_decl_of(feature),
                context,
                context_class,
                types,
            ),
            name=feature.name,
            clients=typed_clients,
        )
    elif isinstance(feature, BaseMethod):
        return make_typed_method(
            feature,
            typed_clients,
            context,
            context_class,
            types,
        )

    raise ValueError


# def make_generics(
#         class_generics: list[GenericSpec],
#         types: TypeScope,
# ) -> dict[str, Type]:
#     type_mapping = {}
#     duplicated = {}
# 
#     for template_name, group in groupby(class_generics, lambda x: x.template_type_name):
#         group = list(group)
# 
#         if len(group) > 1:
#             duplicated[template_name] = group
#             continue
# 
#         generic_spec = group[0]
# 
#         if generic_spec.template_type_name in types:
#             raise ValueError("Invalid generic letter")
# 
#         parent = generic_spec.required_parent
#         if parent is None:
#             parent_name = "ANY"
#         else:
#             if not isinstance(parent, ClassType):
#                 raise ValueError()
#             
#             parent_name = parent.name
# 
#         parent_type = types.find(parent_name)
#         if parent_type is None:
#             print("434", parent_name)
#             raise ValueError()
# 
#         type_mapping[template_name] = parent_type
# 
#     if duplicated:
#         raise ValueError(duplicated)
#     
#     return type_mapping


def type_scope_with_generics(
        type_scope: TypeScope,
        generics: list[GenericSpec],
) -> TypeScope:
    # Проанализировать потом...
    # if fc.decl.generics:
    #     types = TypeScope.from_other_type_scope(types)
    #     type_mapping = make_generics(fc.decl.generics, types)
    #     for generic_name, real_type in type_mapping.items():
    #         types.add_generic_type(generic_name, real_type)
    return type_scope.copy()


def process_stage2(classes: list[FlattenClass]) -> list[TypedClass]:
    # 1. Создаем скоуп-типов с упоминанем всех классов программы
    global_type_scope = TypeScope.from_classes(classes)

    # Добавление костыля в виде класса Void необходимо, чтобы типизировать
    # методы, у которых не указано возвращаемое значение. Никаких ошибок
    # не должно возникнуть, т.к. Void это зарезервированное слово в Eiffel
    void_class = TypedClass(name="Void")
    global_type_scope.add(void_class)

    # 2. Проходимся по каждой фиче из каждого класса и типизируем её
    for fc in classes:
        class_type_scope = type_scope_with_generics(
            global_type_scope,
            fc.decl.generics,
        )

        tc = class_type_scope.find(fc.name)
        assert tc is not None, f"Class {fc.name} not found in type scope: {class_type_scope}"

        features_scope = Scope()
        for _, feature in fc.own_features:
            typed_feature = make_typed_feature(
                feature=feature,
                context=features_scope,
                context_class=tc,
                types=class_type_scope,
            )

            added = features_scope.add(typed_feature)
            assert added, "Should never occur"

        tc.features_scope = features_scope

    # 3. Проходимся по всем классам и устаналиваем родителей
    for fc in classes:
        tc = class_type_scope.find(fc.name)
        assert tc is not None, f"Class {fc.name} not found in type scope: {class_type_scope}"

        parents = [global_type_scope.find(parent.name) for parent in fc.parents]
        assert all(parent is not None for parent in parents), "Should never occur"

        tc.parents = parents

    print(global_type_scope)
