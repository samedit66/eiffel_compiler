
from __future__ import annotations
from dataclasses import dataclass

from ..base import SemanticError

from ...tree.features import Feature


@dataclass
class EffectiveClassHasDeferredFaturesError(SemanticError):
    """Ошибка, возникающая, если эффективный класс содержит отложенные фичи."""
    deferred_features: list[Feature]

    def __str__(self) -> str:
        feature_descriptions = "\n".join(
            f"- {feature.name}: {type(feature).__name__}" for feature in self.deferred_features
        )
        return (
            "The class is effective but contains deferred features.\n"
            "Deferred features:\n"
            f"{feature_descriptions}"
        )
