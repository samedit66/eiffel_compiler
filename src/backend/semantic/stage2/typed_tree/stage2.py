from itertools import groupby

from ....tree.type_decl import *
from ....tree.features import *

from ...stage1 import FlattenClass

from .tables import (
    Type,
    TypeHierarchy,
    FeaturesScope,
    LocalsScope,
)
from .tfeature import *
from .tclass import TypedClass


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
        context: FeaturesScope,
        context_class: FlattenClass,
        types: TypeHierarchy,
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
    if type_ == "NONE":
        raise ValueError("NONE is not allowed as type anywhere")
    
    return type_


def make_locals(
        var_decls: list[Parameter | LocalVarDecl],
        context: FeaturesScope,
        context_class: FlattenClass,
        types: TypeHierarchy, 
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

    parameters = []
    # Добавляем в скоуп параметры метода...
    for local in make_locals(method.parameters, context, context_class, types):
        parameters.append(local)
        added = method_context.add(local)
        assert added, f"Local variable or function parameter must not share same names with features: {local.name}"

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
        parameters=parameters,
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


def process_stage2(classes: list[FlattenClass]) -> list[TypedClass]:
    # 1. Создаем иерархию всех типов в программе
    type_hierarchy = TypeHierarchy.from_classes(classes)

    # Добавление костыля в виде типа Void необходимо, чтобы типизировать
    # методы, у которых не указано возвращаемое значение. Никаких ошибок
    # не должно возникнуть, т.к. Void это зарезервированное слово в Eiffel
    void_type = Type(type_name="Void")
    type_hierarchy.add(void_type)

    # 2. Проходимся по каждой фиче из каждого класса и типизируем её
    typed_classes = []
    for fc in classes:
        class_type = Type(fc.name)

        feature_scope = FeaturesScope()        
        
        implicit_features = fc.features.implicit
        features = fc.features.features

        for _, feature in implicit_features:
            typed_feature = make_typed_feature(
                feature=feature,
                context=features_scope,
                context_class=tc,
                types=class_type_scope,
            )

            added = feature_scope.add(typed_feature)
            assert added, "Should never occur"

        constructors = [
            feature
            for feature in feature_scope
            if feature.name in fc.constructors
        ]

        typed_classes.append(
            TypedClass(
                type_of=class_type,
                is_deferred=fc.is_deferred,
                constructors=constructors,
                feature_scope=feature_scope,
            )
        )

    return global_type_scope.as_list()
