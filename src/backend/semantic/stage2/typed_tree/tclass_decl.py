from dataclasses import dataclass
from pathlib import Path

from .tables import Type, FeaturesScope


@dataclass(kw_only=True)
class TypedClassDecl:
    type_of: Type
    is_deferred: bool
    parents: list[Type]
    constructors: list[TypedFeature]
    feature_scope: FeaturesScope
    defined_in_file: Path | None
