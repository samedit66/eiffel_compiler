from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterator

from ...stage1 import FlattenClass

from .tfeature import TypedFeature, TypedLocal


@dataclass(kw_only=True)
class Type:
    type_name: str
    actual_generics: list[Type] = field(default_factory=list)

    def __eq__(self, other: Type | str) -> bool:
        if isinstance(str, other):
            return self.type_name == other
        return self.type_name == other.type_name 

    def __hash__(self) -> int:
        return hash(self.type_name)


class TypeHierarchy:
    
    def __init__(self) -> None:
        self.types: dict[Type, list[Type]] = defaultdict(list)

    def rememeber(self, child: Type, parent: Type) -> None:
        if parent not in self.types:
            self.types[child].append(parent)

    def find(self, type_name: str) -> Type | None:
        if type_name in self.types:
            return Type(type_name=type_name)
        return None

    def conforms_to(self, child: Type, parent: Type) -> bool:
        if child not in self.types:
            raise ValueError(f"Child type {child} not in type hierarchy")

        parents = self.types[child]
        if parent in parents:
            return True
        
        return any(self.conforms_to(candidate, parent) for candidate in parents)
    
    def __contains__(self, t: Type | str) -> bool:
        if isinstance(type, str):
            t = Type(str)
        return t in self.types

    @staticmethod
    def from_classes(classes: list[FlattenClass]) -> TypeHierarchy:
        hierarchy = TypeHierarchy()

        # Создаем вспомогательную функцию для обработки цепочки наследования
        def process_class(cls: FlattenClass):
            for parent in cls.parents:
                # Добавляем прямое отношение между дочерним и родительским классами
                hierarchy.remember(Type(cls.name), Type(parent.name))
                # Рекурсивно обрабатываем всех родителей
                process_class(parent)

        for cls in classes:
            process_class(cls)

        return hierarchy


class FeaturesScope:
    
    def __init__(self) -> None:
        self.features: dict[str, TypedFeature] = {}

    def add(self, feature: TypedFeature) -> bool:
        if feature.name in self.features:
            return False
        
        self.features[feature.name] = feature
        return True
    
    def find(self, feature_name: str) -> TypedFeature | None:
        return self.features.get(feature_name)
    
    def __contains__(self, name: str) -> bool:
        return self.find(name) is not None
    
    def __repr__(self) -> str:
        return f"[{" ".join(self.features.keys())}]"
    
    def __iter__(self) -> Iterator[TypedFeature]:
        return iter(self.features.values())


class LocalsScope:
    
    def __init__(self) -> None:
        self.locals: dict[str, TypedLocal] = {}

    def add(self, local: TypedLocal) -> bool:
        if local.name in self.locals:
            return False
        
        self.locals[local.name] = local
        return True
    
    def find(self, local_name: str) -> TypedLocal | None:
        return self.locals.get(local_name)
    
    def __contains__(self, name: str) -> bool:
        return self.find(name) is not None
    
    def __repr__(self) -> str:
        return f"[{" ".join(self.locals.keys())}]"
    
    def __iter__(self) -> Iterator[TypedLocal]:
        return iter(self.locals.values())
