from dataclasses import dataclass
from pathlib import Path

from .tables import Type, FeaturesScope
from .tfeature import TypedFeature


@dataclass(kw_only=True)
class TypedClass:
    type_of: Type
    is_deferred: bool
    constructors: list[TypedFeature]
    feature_scope: FeaturesScope
