from __future__ import annotations
from collections import defaultdict
from itertools import groupby
from typing import Iterator

from ...tree.features import (
    Feature,
    Method,
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
        self.feature_set.pop(feature_name)

    def get(self, feature_name: str) -> Feature | None:
        return self.feature_set.get(feature_name, None)

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
        duplicated: dict[str, list[Feature]] = defaultdict(list)

        for feature in features:
            try:
                feature_set.add(feature.name, feature)
            except FeatureAlreadyInError:
                feature_in = feature_set.get(feature.name)

                # Успешные случаи:
                # 1) В feature_set записана отложенной фича и сама feature
                #    является отложенной (добавления при этом не происходит)
                # 2) В feature_set записана отложенная фича, а сама feature
                #    является эффективной
                # 3) В feature_set записана эффективная фича, а сама feature
                #    является абстрактной (добавления при это не происходит)
                # В любом другом случае добавление приводит к возникновению исключения

                if (isinstance(feature_in, Method) and feature_in.is_deferred
                        and isinstance(feature, Method) and feature.is_deferred):
                    pass
                elif (isinstance(feature_in, Method) and feature_in.is_deferred
                        and (not isinstance(feature, Method) or not feature.is_deferred)):
                    feature_set.remove(feature.name)
                    feature_set.add(feature.name, feature)
                elif ((not isinstance(feature_in, Method) or not feature_in.is_deferred)
                        and isinstance(feature, Method) and feature.is_deferred):
                    pass
                else:
                    duplicated[feature.name].append(feature)

        if duplicated:
            # Костыль: при повторении надо учитывать все повторяющиеся версии,
            # но самая первая версия остается в feature_set, поэтому ее надо оттуда взять
            for feature_name, feature in feature_set:
                if feature_name in duplicated:
                    duplicated[feature_name].append(feature)

            raise DuplicateFeaturesError(duplicated)

        return feature_set
