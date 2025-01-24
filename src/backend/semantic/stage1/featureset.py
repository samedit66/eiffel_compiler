from __future__ import annotations
from itertools import groupby
from typing import Iterator

from ...tree.features import (
    Feature,
    Method,
    Field,
    Constant,
    )

from ..base import SemanticError


class FeatureAlreadyInError(ValueError):
    ...


class DuplicateFeaturesError(SemanticError):
    ...


class FeatureSet:

    def __init__(self) -> None:
        self.feature_set: dict[str, Feature] = {}

    def add(self, feature_name: str, feature: Feature) -> None:
        if feature_name in self.feature_set:
            raise FeatureAlreadyInError(feature_name, feature)
        self.feature_set[feature_name] = feature

    def remove(self, feature_name: str) -> None:
        del self.feature_set[feature_name]

    def __contains__(self, feature_name: str) -> bool:
        return feature_name in self.feature_set

    def __iter__(self) -> Iterator[tuple[str, Feature]]:
        return iter(self.feature_set.items())

    def __repr__(self) -> str:
        return f"[{" ".join(self.feature_set.keys())}]"

    def __bool__(self) -> bool:
        return bool(self.feature_set)

    @staticmethod
    def union(*sets: FeatureSet) -> FeatureSet:
        all_features: list[Feature] = []
        for feature_set in sets:
            for _, feature in feature_set:
                all_features.append(feature)
        return FeatureSet.parse(all_features)

    @staticmethod
    def parse(features: list[Feature]) -> FeatureSet:
        """Создает множество фич из заданного списка фич.
        Гарантирует, что все фичи являются уникальными - дублирование
        имен отсутствует.
        """
        feature_set = FeatureSet()
        duplicated: dict[str, list[Feature]] = {}

        for feature_name, feature_group in groupby(features, key=lambda feature: feature.name):
            feature_group = list(feature_group)

            if len(feature_group) == 1:
                feature_set.add(feature_name, feature_group[0])
                continue

            # Особый случай слияния заключается в следующей ситуации:
            # имеется несколько одинаково названных фич, причем одна из них
            # эффективная (определенная), а все остальные - абстрактные (отложенные).
            # Данная ситуация ошибкой не считается, т.к. доступна только одна реализация.
            # Помимо этого сюда подпадает и случай, когда всего лишь одна 
            # эффективная фича и нет отложенных
            effective = [
                feature
                for feature in feature_group
                if not isinstance(feature, Method) or not feature.is_deferred
            ]
            if len(effective) == 1 and len(feature_group) >= 1:
                feature_set.add(feature_name, effective[0])
                continue

            # Ошибочная ситуация - несколько одноименных фич, причем более одной
            # из них имеют одну и ту же реализацию
            duplicated[feature_name] = feature_group

        if duplicated:
            raise DuplicateFeaturesError(duplicated)

        return feature_set
