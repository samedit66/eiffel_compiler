from __future__ import annotations
from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from itertools import groupby

from ...tree.features import (
    Constant,
    Field,
    BaseMethod,
    Method,
    Feature,
    LocalVarDecl,
    Parameter,
)
from ...tree.type_decl import (
    TypeDecl,
    ClassType,
    TupleType,
    LikeCurrent,
    LikeFeature,
    GenericSpec,
)
from ...tree.expr import Expr

from ..stage1 import FlattenClass
from ..stage1.ftable import FeatureSet


@dataclass(kw_only=True)
class TypeScope:
    defined_types: dict[str, TypedClass] = field(default_factory=dict)

    def add(self, new_type: TypedClass, type_name: str | None = None) -> bool:
        if type_name is None:
            type_name = new_type.name

        if type_name in self.defined_types:
            return False
        
        self.defined_types[type_name] = new_type
        return True

    def find(self, type_name: str) -> TypedClass | None:
        return self.defined_types.get(type_name)
    
    def copy(self) -> TypeScope:
        defined_types = self.defined_types.copy()
        return TypeScope(defined_types=defined_types)

    def as_list(self) -> list[TypedClass]:
        return list(self.defined_types.values())

    def __contains__(self, type_name: str) -> bool:
        return self.find(type_name) is not None

    def __iter__(self):
        return iter(self.defined_types.values())

    @staticmethod
    def from_classes(classes: list[FlattenClass]) -> TypeScope:
        type_scope = TypeScope()
        for tc in classes:
            type_scope.add(TypedClass(name=tc.name))
        return type_scope


@dataclass(kw_only=True)
class Binding(ABC):
    type_of: TypedClass
    name: str


class Scope:
    bindings: dict[str, Binding]
    parent_scope: Scope | None = None
    
    def __init__(self, parent_scope: Scope | None = None):
        self.bindings = {}
        self.parent_scope = parent_scope

    def add(self, binding: Binding) -> bool:
        if binding.name in self.bindings:
            return False
        
        self.bindings[binding.name] = binding
        return True

    def find(self, name: str) -> Binding | None:
        binding = self.bindings.get(name)

        if binding is not None:
            return binding

        if self.parent_scope is None:
            return None
        
        return self.parent_scope.find(name)
    
    def __contains__(self, name: str) -> bool:
        return self.find(name) is not None
    
    def __repr__(self) -> str:
        return f"[{" ".join(self.bindings.keys())}]"
    
    def __iter__(self):
        return iter(self.bindings.values())


@dataclass(kw_only=True)
class TypedFeature(Binding, ABC):
    clients: list[TypedClass]


@dataclass(kw_only=True)
class TypedConstant(TypedFeature):
    value: Expr


@dataclass(kw_only=True)
class TypedField(TypedFeature):
    ...


@dataclass(kw_only=True)
class TypedLocal(Binding):
    ...


@dataclass(kw_only=True)
class TypedMethod(TypedFeature):
    name: str
    method_ref: BaseMethod
    local_scope: Scope
    parameters: list[TypedLocal] = field(default_factory=list)


class TypedClass:

    def __init__(
            self, 
            name: str,
            features_scope: Scope | None = None,
            parents: list[TypedClass] | None = None,
    ) -> None:
        self.name = name
        self.features_scope = features_scope or Scope()
        self.parents = parents or []

    def __eq__(self, other_class: TypedClass) -> bool:
        return self.name == other_class.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"\"Class {self.name}, features {self.features_scope}\""

    def iterfeatures(self):
        return iter(self.features_scope)

    def responds_to(self, feature_name: str, caller: TypedClass) -> bool:
        feature = self.features_scope.find(feature_name)
        if feature is None:
            return False
        
        assert isinstance(feature, TypedFeature), "Should never occur"

        return any(caller.conforms_to(client) for client in feature.clients)

    def conforms_to(self, other_class: TypedClass) -> bool:
        # Дикий костыль... 
        if self.name == "NONE":
            return False

        if self == other_class:
            return True
        return any(parent.conforms_to(other_class) for parent in self.parents)

    @staticmethod
    def common_ancestor(classes: list[TypedClass]) -> TypedClass | None:
        """
        Находит ближайший общий предок для списка классов.

        :param classes: список объектов TypedClass
        :return: ближайший общий предок или None, если его нет
        """
        if not classes:
            return None

        # Функция для получения всех предков класса с их уровнями глубины
        def get_ancestors_with_depth(cls: TypedClass, depth: int = 0, ancestors: dict = None) -> dict[TypedClass, int]:
            ancestors = ancestors or {}
            ancestors[cls] = depth
            for parent in cls.parents:
                if parent not in ancestors or ancestors[parent] > depth + 1:
                    get_ancestors_with_depth(parent, depth + 1, ancestors)
            return ancestors

        # Получаем предков первого класса с глубиной
        common_ancestors = get_ancestors_with_depth(classes[0])

        # Пересекаем предков с предками остальных классов
        for cls in classes[1:]:
            current_ancestors = get_ancestors_with_depth(cls)
            common_ancestors = {
                ancestor: min(common_ancestors[ancestor], current_ancestors[ancestor])
                for ancestor in common_ancestors.keys() & current_ancestors.keys()
            }

        # Если пересечение пустое, то общего предка нет
        if not common_ancestors:
            return None

        # Найти ближайшего общего предка (с минимальной глубиной)
        return min(common_ancestors, key=common_ancestors.get)
