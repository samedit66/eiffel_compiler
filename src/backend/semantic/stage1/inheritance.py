from __future__ import annotations
from collections import namedtuple, defaultdict
import copy
from dataclasses import dataclass
from itertools import groupby

from ...tree.class_decl import ClassDecl, Parent, Alias
from ...tree.features import Feature, Field, Constant, Method

from .errors import EffectiveClassHasDeferredFaturesError


@dataclass(kw_only=True)
class FRecord:
    class_name: str
    feature: Feature
    
    @property
    def name(self):
        return self.feature.name
    
    def __eq__(self, other: FRecord | str) -> bool:
        # Костыль для того, чтобы в типе list[FRecord] можно было проверять
        # наличие фичи по ее имени
        if isinstance(other, str):
            return self.name == other

        return self.class_name == other.class_name and self.name == other.name


type RenameRules = dict[str, str]


def rename_rules_parse(
        parent: list[FRecord],
        child: list[FRecord],
        aliases_list: list[Alias],
) -> RenameRules:
    if not aliases_list:
        return {}

    duplicated_originals = {
        original_name: aliases
        for original_name, aliases in groupby(aliases_list, key=lambda alias: alias.original_name)
        if sum(1 for _ in aliases) > 1
    }
    if duplicated_originals: raise ValueError()

    duplicated_aliases = {
        alias_name: aliases
        for alias_name, aliases in groupby(aliases_list, key=lambda alias: alias.alias_name)
        if sum(1 for _ in aliases) > 1
    }
    if duplicated_aliases: raise ValueError()

    nonexistent_features = {
        alias.original_name: alias
        for alias in aliases_list
        if alias.original_name not in parent
    }
    if nonexistent_features:
        print(parent)
        raise ValueError(nonexistent_features)

    # Название обманывает: в данный словарь могут быть
    # помещены не только определенные (effective) фичи, но и
    # те, который объявлены как deferred, т.е. любые фичи,
    # которые появляются в определении дочернего класса
    already_defined = {}
    for alias in aliases_list:
        for child_record in child:
            if child_record.name == alias.alias_name:
                already_defined[alias] = child_record.feature
    if already_defined:
        raise ValueError()

    rules: RenameRules = {}
    for alias in aliases_list:
        rules[alias.original_name] = alias.alias_name

    return rules


def rename(
        child_name: str,
        parent: list[FRecord], 
        rules: RenameRules,
) -> tuple[list[FRecord], list[FRecord]]:
    if not rules:
        return [], parent

    # Оригинальные фичи родителя, которые были переименованы
    renamed: list[FRecord] = []
    # Обновленные фичи родителя
    new_parent: list[FRecord] = []

    for record in parent:
        if record.name in rules:
            renamed.append(record)

            renamed_feature = copy.replace(record.feature, name=rules[record.name])
            new_parent.append(
                FRecord(class_name=child_name, feature=renamed_feature)
            )
        else:
            new_parent.append(record)

    return renamed, new_parent


UndefineRules = namedtuple("UndefineRules", "to_undefine deferred_features")


def undefine_rules_parse(
        parent: list[FRecord],
        other_parents: list[list[FRecord]],
        child: list[FRecord],
        to_undefine: list[str],
        is_child_deferred: bool,
) -> UndefineRules:
    if not to_undefine:
        return UndefineRules(to_undefine=[], deferred_features={})

    duplicated = [
        feature_name
        for feature_name in to_undefine
        if to_undefine.count(feature_name) > 1
    ]
    if duplicated: raise ValueError()

    nonexistent = [
        feature_name
        for feature_name in to_undefine
        if feature_name not in parent
    ]
    if nonexistent: raise ValueError()

    nondefined_anywhere = [
        feature_name
        for feature_name in to_undefine
        if all(feature_name not in parents_features for parents_features in other_parents)
            and feature_name not in child
            and feature_name not in parent
    ]
    if not is_child_deferred and nondefined_anywhere: raise ValueError()
    
    features_to_defer = {
        record.name: record.feature
        for record in parent
        if all(record.name not in records for records in other_parents)
            and record.name not in child
            and record.name in to_undefine
    }

    constants_to_defer = {
        feature_name: feature
        for feature_name, feature in features_to_defer.items()
        if isinstance(feature, Constant)
    }
    if constants_to_defer:
        raise ValueError()

    # Возможно здесь можно и без словаря обойтись,
    # а просто список возвращать
    deferred_features = {}
    for feature_name, feature in features_to_defer.items():
        # Если поле было undefined, то преобразуем его в отложенный метод
        if isinstance(feature, Field):
            feature = Method(
                location=feature.location,
                name=feature.name,
                clients=feature.clients,
                is_deferred=True,
                return_type=feature.value_type,
                )
        elif isinstance(feature, Method):
            feature = copy.replace(feature, is_deferred=True)

        deferred_features[feature_name] = feature

    return UndefineRules(
        to_undefine=to_undefine,
        deferred_features=deferred_features,
    )


def undefine(
        parent: list[FRecord],
        rules: UndefineRules,
) -> list[FRecord]:
    if not rules.to_undefine:
        return parent
    
    reduced_features = []

    for record in parent:
        if record.name not in rules.to_undefine:
            reduced_features.append(record)

    return reduced_features


type RedefineRules = dict[str, FRecord]


def redefine_rules_parse(
        parent: list[FRecord],
        child: list[FRecord],
        to_redefine: list[str],
) -> RedefineRules:
    if not to_redefine:
        return {}

    duplicated = [
        feature_name
        for feature_name in to_redefine
        if to_redefine.count(feature_name) > 1
    ]
    if duplicated:
        raise ValueError()

    nonexistent_in_parent = [
        feature_name
        for feature_name in to_redefine
        if feature_name not in parent
    ]
    if nonexistent_in_parent:
        raise ValueError()
    
    nonredefined_in_child = [
        feature_name
        for feature_name in to_redefine
        if feature_name not in child
    ]
    if nonredefined_in_child:
        raise ValueError()
    
    constants_to_redefine = {
        record.name: record.feature
        for record in parent
        if isinstance(record.feature, Constant) and record.name in to_redefine
    }
    if constants_to_redefine:
        raise ValueError()

    redefine_rules = {}
    for record in parent:
        if record.name in to_redefine:
            redefine_rules[record.name] = f"<Precursor_{record.name}>"
    
    return redefine_rules


def redefine(
        parent: list[FRecord],
        rules: RedefineRules,
) -> list[FRecord]:
    if not rules:
        return parent
    
    new_parent = []

    for record in parent:
        if record.name in rules:
            renamed_feature = copy.replace(record.feature, name=rules[record.name])
            new_parent.append(
                FRecord(class_name=record.class_name, feature=renamed_feature)
            )
        else:
            new_parent.append(record)

    return new_parent


type SelectRules = list[str]


def select_rules_parse(
        parent: list[FRecord],
        other_parents: list[list[FRecord]],
        child: list[FRecord],
        to_select: list[str],
) -> SelectRules:
    if not to_select:
        return set()

    duplicates = [
        feature_name
        for feature_name in to_select
        if to_select.count(feature_name) > 1
    ]
    if duplicates:
        raise ValueError()
    
    nonexistent_in_parent = [
        feature_name
        for feature_name in to_select
        if feature_name not in parent
    ]
    if nonexistent_in_parent:
        raise ValueError()
    
    nonexistent_in_other_parents = [
        feature_name
        for feature_name in to_select
        if all(feature_name not in records for records in other_parents)
    ]
    if nonexistent_in_other_parents:
        raise ValueError()
    
    already_in_child = [
        feature_name
        for feature_name in to_select
        if feature_name in child
    ]
    if already_in_child:
        raise ValueError()
    
    return to_select


def select(
        other_parents: list[list[FRecord]],
        select_rules: SelectRules,
) -> list[list[FRecord]]:
    if not select_rules:
        return other_parents

    filtered_parents = []

    for parent in other_parents:
        new_parent = []

        for record in parent:
            if record.name not in select_rules:
                new_parent.append(record)

        filtered_parents.append(new_parent)

    return filtered_parents


def parse_constructors(
        constructors: list[str],
        features: list[FRecord],
) -> list[Method]:
    nonexistent = []

    found: list[Method] = []
    for constructor_name in constructors:
        if constructor_name not in features:
            nonexistent.append(constructor_name)
            continue

        cf = next(f for f in features if f.name == constructor_name)
        found.append(cf)

    if nonexistent:
        raise ValueError(nonexistent)
    
    not_methods = []
    for cf in found:
        if not isinstance(cf, Method):
            not_methods.append(cf)

    if not_methods:
        raise ValueError(not_methods)
    
    return found


FTable = namedtuple("FTable", "implicit features")

Transforms = namedtuple("Transforms", "rename undefine redefine select")


def to_records(class_decl: ClassDecl) -> list[FRecord]:
    return [
        FRecord(
            class_name=class_decl.class_name,
            feature=feature,
        )
        for feature in class_decl.features
    ]


def ftable_of(parent: Parent) -> FTable:
    if not parent.class_decl.inherit:
        return FTable(implicit=[], features=to_records(parent.class_decl))
    return analyze_inheritance(parent.class_decl)


def merge(*tables: list[FRecord]) -> list[FRecord]:
    all_features = [
        feature
        for table in tables
        for feature in table
    ]

    duplicates: dict[str, list[FRecord]] = {}

    groups: dict[str, list[FRecord]] = defaultdict(list)
    for record in all_features:
        # Проверяем, есть ли уже такая фича в группе
        if record not in groups[record.name]:
            groups[record.name].append(record)

    merged = []
    for feature_name, group in groups.items():
        effective = [
            record
            for record in group
            if not isinstance(record.feature, Method)
                or not record.feature.is_deferred
        ]

        if len(effective) == 1:
            merged.append(effective[0])
            continue

        deferred = [
            record
            for record in group
            if isinstance(record.feature, Method)
                and record.feature.is_deferred
        ]

        if len(effective) == 0 and len(deferred) > 0:
            merged.append(deferred[0])
            continue
        
        duplicates[feature_name] = list(group)

    if duplicates:
        raise ValueError(duplicates)

    return merged


def analyze_inheritance(class_decl: ClassDecl) -> FTable:
    child_name = class_decl.class_name
    child_features = to_records(class_decl)

    # 0 этап: (возможно, должен быть не тут): проверка того, что 
    # все указанные конструкторы существуют
    parse_constructors(class_decl.create, child_features)

    parents_tables: dict[str, FTable] = {
        parent.class_name: ftable_of(parent)
        for parent in class_decl.inherit
    }

    parent_transforms: dict[str, Transforms] = {
        parent.class_name: Transforms(
            rename=parent.rename,
            undefine=parent.undefine,
            redefine=parent.redefine,
            select=parent.select,
        )
        for parent in class_decl.inherit
    }

    # 1 этап: rename
    renamed_features: dict[str, list[FRecord]] = {}
    for parent_name, parent_table in parents_tables.items():

        rename_rules = rename_rules_parse(
            parent=parent_table.features,
            child=child_features,
            aliases_list=parent_transforms[parent_name].rename,
        )

        renamed, new_parent_features = rename(
            child_name=child_name,
            parent=parent_table.features,
            rules=rename_rules,
        )

        renamed_features[parent_name] = renamed

        new_parent_table = FTable(
            implicit=parent_table.implicit,
            features=new_parent_features,
        )
        parents_tables[parent_name] = new_parent_table

    # 2 этап: undefine
    for parent_name, parent_table in parents_tables.items():
        other_tables = [
            table.features
            for class_name, table in parents_tables.items()
            if class_name != parent_name
        ]

        undefine_rules = undefine_rules_parse(
            parent=parent_table.features,
            other_parents=other_tables,
            child=child_features,
            to_undefine=parent_transforms[parent_name].undefine,
            is_child_deferred=class_decl.is_deferred,
        )

        new_parent_features = undefine(
            parent=parent_table.features,
            rules=undefine_rules,
        )

        new_parent_table = FTable(
            implicit=parent_table.implicit,
            features=new_parent_features,
        )
        parents_tables[parent_name] = new_parent_table

         # Добавляем отложенные фичи
        for _, feature in undefine_rules.deferred_features.items():
            child_features.append(
                FRecord(class_name=child_name, feature=feature)
            )
    
    # 3 этап: redefine
    for parent_name, parent_table in parents_tables.items():
        redefine_rules = redefine_rules_parse(
            parent=parent_table.features,
            child=child_features,
            to_redefine=parent_transforms[parent_name].redefine,
        )

        new_parent_features = redefine(
            parent=parent_table.features,
            rules=redefine_rules,
        )

        new_parent_table = FTable(
            implicit=parent_table.implicit,
            features=new_parent_features,
        )
        parents_tables[parent_name] = new_parent_table

    # 4 этап: select
    for parent_name, parent_table in parents_tables.items():
        if len(parents_tables) == 1: break

        pairs = ([
            (class_name, table.features)
            for class_name, table in parents_tables.items()
            if class_name != parent_name
        ])
        other_names = [p[0] for p in pairs]
        other_features = [p[1] for p in pairs] 

        select_rules = select_rules_parse(
            parent=parent_table.features,
            other_parents=other_features,
            child=child_features,
            to_select=parent_transforms[parent_name].select,
        )

        new_other_features = select(
            other_parents=other_features,
            select_rules=select_rules,
        )

        assert len(other_features) == len(new_other_features), "Should never occur"

        for other_name, new_features in zip(other_names, new_other_features):
            new_parent_table = FTable(
                implicit=parents_tables[other_name].implicit,
                features=new_features,
            )
            parents_tables[other_name] = new_parent_table

    # 5 этап: слияние всех фич
    implicit: list[FRecord] = []
    for _, record in renamed_features.items():
        implicit.extend(record)

    merged = merge(
        child_features,
        *[table.features for _, table in parents_tables.items()]
    )

    # 6 этап: проверка, что у effective класса отсутствуют deferred фичи
    deferred = [
        record.feature
        for record in implicit + merged
        if isinstance(record.feature, Method) and  record.feature.is_deferred
    ]
    if deferred and not class_decl.is_deferred:
        raise EffectiveClassHasDeferredFaturesError(deferred)

    return FTable(implicit=implicit, features=merged)
