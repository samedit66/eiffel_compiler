from __future__ import annotations
from itertools import groupby
from typing import Iterator

from ...tree.features import Feature

from ..base import SemanticError


class FeatureAlreadyInError(ValueError):
    ...


class DuplicatedFeaturesError(SemanticError):
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
            if len(feature_group) > 1:
                duplicated[feature_name] = feature_group
                continue

            # Обработки try/except на FeatureAlreadyInError нет,
            # т.к. groupby группирует повторяющиеся фичи
            feature_set.add(feature_name, feature_group[0])

        if duplicated:
            raise DuplicatedFeaturesError(duplicated)

        return feature_set
