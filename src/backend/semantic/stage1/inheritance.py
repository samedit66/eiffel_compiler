from __future__ import annotations
from collections import namedtuple
import copy
from dataclasses import dataclass
from itertools import groupby

from ...tree.class_decl import ClassDecl, Parent, Alias
from ...tree.features import Field, Constant, Method

from .featureset import FeatureSet, FeatureAlreadyInError


type RenameRules = dict[str, str]


def rename_rules_parse(
        parent_set: FeatureSet,
        child_set: FeatureSet,
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
        if alias.original_name not in parent_set
    }
    if nonexistent_features: raise ValueError()

    # Название обманывает: в данный словарь могут быть
    # помещены не только определенные (effective) фичи, но и
    # те, который объявлены как deferred, т.е. любые фичи,
    # которые появляются в определении дочернего класса
    already_defined = {}
    for alias in aliases_list:
        for feature_name, feature in child_set:
            if feature_name == alias.alias_name:
                already_defined[alias] = feature
    if already_defined:
        raise ValueError()

    rules: RenameRules = {}
    for alias in aliases_list:
        rules[alias.original_name] = alias.alias_name

    return rules


def rename(
        parent_set: FeatureSet, 
        rules: RenameRules,
) -> FeatureSet:
    if not rules:
        return parent_set

    renamed_feature_set = FeatureSet()

    for feature_name, feature in parent_set:
        feature_name = rules.get(feature_name, feature_name)
        renamed_feature = copy.replace(feature, name=feature_name)
        renamed_feature_set.add(feature_name, renamed_feature)

    return renamed_feature_set


UndefineRules = namedtuple("UndefineRules", "to_undefine deferred_features")


def undefine_rules_parse(
        parent_set: FeatureSet,
        other_parents_sets: list[FeatureSet],
        child_set: FeatureSet,
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
        if feature_name not in parent_set
    ]
    if nonexistent: raise ValueError()

    nondefined_anywhere = [
        feature_name
        for feature_name in to_undefine
        if all(feature_name not in feature_set for feature_set in other_parents_sets)
            and feature_name not in child_set
    ]
    if not is_child_deferred and nondefined_anywhere: raise ValueError()
    
    deferred_features = {
        feature_name: feature
        for feature_name, feature in parent_set
        if feature_name in nondefined_anywhere
    }

    deferred_constants = {
        feature_name: feature
        for feature_name, feature in deferred_features.items()
        if isinstance(feature, Constant)
    }
    if deferred_constants:
        raise ValueError()

    converted = {}
    for feature_name, feature in deferred_features.items():
        # Если поле было undefined, то преобразуем его в отложенный метод
        if isinstance(feature, Field):
            feature = Method(
                location=feature.location,
                name=feature.name,
                clients=feature.clients,
                is_deferred=True,
                return_type=feature.value_type,
                )
        converted[feature_name] = feature

    return UndefineRules(
        to_undefine=to_undefine,
        deferred_features=converted,
    )


def undefine(
        parent_set: FeatureSet,
        rules: UndefineRules,
) -> FeatureSet:
    if not rules.to_undefine:
        return parent_set
    
    reduced_features = FeatureSet()

    for feature_name, feature in parent_set:
        if feature_name not in rules.to_undefine:
            reduced_features.add(feature_name, feature)

    return reduced_features


type RedefineRules = FeatureSet


def redefine_rules_parse(
        parent_set: FeatureSet,
        child_set: FeatureSet,
        to_redefine: list[str],
) -> RedefineRules:
    if not to_redefine:
        return FeatureSet()

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
        if feature_name not in parent_set
    ]
    if nonexistent_in_parent:
        raise ValueError()
    
    nonredefined_in_child = [
        feature_name
        for feature_name in to_redefine
        if feature_name not in child_set
    ]
    if nonredefined_in_child:
        raise ValueError()
    
    redefine_rules = FeatureSet()
    for feature_name, feature in child_set:
        if feature_name in to_redefine:
            redefine_rules.add(feature_name, feature)
    
    return redefine_rules


def redefine(
        parent_set: FeatureSet,
        rules: RedefineRules,
) -> FeatureSet:
    if not rules:
        return parent_set
    
    redefined_feature_set = FeatureSet.union(rules)

    for feature_name, feature in parent_set:
        if feature_name not in redefined_feature_set:
            redefined_feature_set.add(feature_name, feature)

    return redefined_feature_set


type SelectRules = set[str]


def select_rules_parse(
        parent_set: FeatureSet,
        other_parents_sets: list[FeatureSet],
        child_set: FeatureSet,
        to_select: list[str],
) -> SelectRules:
    if not to_select:
        return set()

    duplicated = [
        feature_name
        for feature_name in to_select
        if to_select.count(feature_name) > 1
    ]
    if duplicated:
        raise ValueError()
    
    nonexistent_in_parent = [
        feature_name
        for feature_name in to_select
        if feature_name not in parent_set
    ]
    if nonexistent_in_parent:
        raise ValueError()
    
    nonexistent_in_other_parents = [
        feature_name
        for feature_name in to_select
        if all(feature_name not in feature_set for feature_set in other_parents_sets)
    ]
    if nonexistent_in_other_parents:
        raise ValueError()
    
    already_in_child = [
        feature_name
        for feature_name in to_select
        if feature_name in child_set
    ]
    if already_in_child:
        raise ValueError()
    
    return set(to_select)


def select(
        other_parents_sets: list[FeatureSet],
        select_rules: SelectRules,
) -> list[FeatureSet]:
    if not select_rules:
        return other_parents_sets

    unselected_parents_sets = []

    for parent_set in other_parents_sets:
        new_parent_set = FeatureSet()

        for feature_name, feature in parent_set:
            if feature_name not in select_rules:
                new_parent_set.add(feature_name, feature)
        
        unselected_parents_sets.append(new_parent_set)

    return unselected_parents_sets


@dataclass(kw_only=True)
class InheritanceInfo:
    class_decl: ClassDecl
    feature_set: FeatureSet
    rename: list[Alias]
    undefine: list[str]
    redefine: list[str]
    select: list[str]

    @property
    def class_name(self) -> str:
        return self.class_decl.class_name


def inheritance_info_parse(parent: Parent) -> InheritanceInfo:
    feature_set = (
        analyze_inheritance(parent.class_decl)
        if parent.class_decl.inherit
        else FeatureSet.parse(parent.class_decl.features)
    )

    return InheritanceInfo(
        class_decl=parent.class_decl,
        feature_set=feature_set,
        rename=parent.rename,
        undefine=parent.undefine,
        redefine=parent.redefine,
        select=parent.select,
    )


def analyze_inheritance(class_decl: ClassDecl) -> FeatureSet:
    child_set = FeatureSet.parse(class_decl.features)

    inheritance_list = [
        inheritance_info_parse(parent)
        for parent in class_decl.inherit
    ]

    # 1 этап: rename
    for inheritance in inheritance_list:
        rename_rules = rename_rules_parse(
            parent_set=inheritance.feature_set,
            child_set=child_set,
            aliases_list=inheritance.rename,
        )
        inheritance.feature_set = rename(
            parent_set=inheritance.feature_set,
            rules=rename_rules,
        )

    # 2 этап: undefine
    for inheritance in inheritance_list:
        undefine_rules = undefine_rules_parse(
            parent_set=inheritance.feature_set,
            other_parents_sets=[
                other_set
                for other_set in [
                    info.feature_set
                    for info in inheritance_list
                    if info.class_decl.class_name != inheritance.class_name
                ]
            ],
            child_set=child_set,
            to_undefine=inheritance.undefine,
            is_child_deferred=inheritance.class_decl.is_deferred,
        )
        inheritance.feature_set = undefine(
            parent_set=inheritance.feature_set,
            rules=undefine_rules,
        )

        # Добавляем отложенные фичи
        for feature_name, feature in undefine_rules.deferred_features.items():
            child_set.add(feature_name, feature)

    # 3 этап: redefine
    for inheritance in inheritance_list:
        redefine_rules = redefine_rules_parse(
            parent_set=inheritance.feature_set,
            child_set=child_set,
            to_redefine=inheritance.redefine,
        )
        inheritance.feature_set = redefine(
            parent_set=inheritance.feature_set,
            rules=redefine_rules,
        )

        # Удаляем переопределенные фичи из изначального child_set
        for feature_name, _ in redefine_rules:
            child_set.remove(feature_name)

    # 4 этап: select
    for inheritance in inheritance_list:
        other_inheritances = [
            other_inheritance
            for other_inheritance in inheritance_list
            if other_inheritance.class_decl.class_name != inheritance.class_name
        ]
        
        other_parents_sets = [
            other_inheritance.feature_set
            for other_inheritance in other_inheritances
        ]

        select_rules = select_rules_parse(
            parent_set=inheritance.feature_set,
            other_parents_sets=other_parents_sets,
            child_set=child_set,
            to_select=inheritance.select,
        )
        other_parents_sets = select(
            other_parents_sets=other_parents_sets,
            select_rules=select_rules,
        )

        assert len(other_inheritances) == len(other_parents_sets)

        for other_inheritance, other_set in zip(other_inheritances, other_parents_sets):
            other_inheritance.feature_set = other_set

    # 5 этап: слияние всех родительских фич
    child_set = FeatureSet.union(
        child_set,
        *[inheritance.feature_set for inheritance in inheritance_list],
    )
    
    return child_set