from ...stage1 import FlattenClass

from .tables import (
    Type,
    TypeHierarchy,
    FeaturesScope,
    LocalsScope,
)


def process_stage2(classes: list[FlattenClass]):
    # 1. Создаем иерархию всех типов в программе
    type_hierarchy = TypeHierarchy.from_classes(classes)

    # Добавление костыля в виде класса Void необходимо, чтобы типизировать
    # методы, у которых не указано возвращаемое значение. Никаких ошибок
    # не должно возникнуть, т.к. Void это зарезервированное слово в Eiffel
    void_type = Type(type_name="Void")
    type_hierarchy.add(void_type)

    typed_classes = []

    # 2. Проходимся по каждой фиче из каждого класса и типизируем её
    for fc in classes:
        # class_type_scope = type_scope_with_generics(
        #     global_type_scope,
        #     fc.decl.generics,
        # )

        features_scope = FeaturesScope()

        tc = class_type_scope.find(fc.name)
        assert tc is not None, f"Class {fc.name} not found in type scope: {class_type_scope}"

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

    type_check(global_type_scope)

    return global_type_scope.as_list()
